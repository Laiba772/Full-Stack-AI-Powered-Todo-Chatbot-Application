from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime, timezone
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.conversation import Conversation
from src.models.message import Message, Sender
from src.schemas.task import UpdateTaskInput, AddTaskInput
from src.api.routes.tasks import TaskService
from openai import OpenAI
from fastapi import HTTPException


class ChatService:
    """
    Service for managing chat conversations and message persistence.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_conversation(self, user_id: UUID) -> Conversation:
        stmt = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        conversation = (await self.session.exec(stmt)).first()
        if not conversation:
            conversation = await self.create_conversation(user_id, title="New Chat")
        return conversation

    async def create_conversation(self, user_id: UUID, title: Optional[str] = None) -> Conversation:
        conversation = Conversation(user_id=user_id, title=title)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        result = await self.session.exec(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.first()

    async def get_messages(self, conversation_id: UUID) -> List[Message]:
        result = await self.session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp)
        )
        return result.all()

    async def add_message(
        self,
        conversation_id: UUID,
        sender: Sender,
        content: str,
        tool_calls: Optional[str] = None,
        tool_output: Optional[Dict] = None
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            sender=sender,
            content=content,
            tool_calls=tool_calls,
            tool_output=tool_output
        )
        self.session.add(message)

        # Update conversation timestamp
        conversation = await self.get_conversation(conversation_id)
        if conversation:
            conversation.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            self.session.add(conversation)

        await self.session.commit()
        await self.session.refresh(message)
        if conversation:
            await self.session.refresh(conversation)

        return message

    async def handle_message(
        self,
        user_id: UUID,
        message: str,
        task_service: TaskService,
        openai_client: OpenAI,
        openai_tools: List[Dict]
    ) -> str:
        """
        Handles a user message, updates tasks if necessary, and adds AI responses.
        """
        # 1. Get or create conversation
        conversation = await self.get_or_create_conversation(user_id)

        # 2. Add user message to conversation
        await self.add_message(
            conversation_id=conversation.id,
            sender=Sender.USER,
            content=message
        )

        lower_message = message.lower()
        response = ""

        # 3. Handle task intents
        if any(word in lower_message for word in ['add', 'create', 'new']) and any(word in lower_message for word in ['task', 'todo']):
            import re
            task_match = re.search(r'(?:add|create|new)\s+(?:a\s+)?(.+)', message, re.IGNORECASE)
            task_title = task_match.group(1).strip() if task_match else "New task"

            task_input = AddTaskInput(title=task_title, description=f"Created via AI assistant: {message}")
            created_task = await task_service.create_task(user_id, task_input)
            response = f"✅ Successfully added task: '{created_task.title}'"

        elif any(word in lower_message for word in ['list', 'show', 'my', 'all']) and any(word in lower_message for word in ['task', 'tasks', 'todo']):
            tasks = await task_service.get_tasks(user_id)
            if tasks:
                task_list = "\n".join([f"• {task.title} ({'✓ Completed' if task.completed else '○ Pending'})" for task in tasks])
                response = f"📋 Your Tasks:\n{task_list}"
            else:
                response = "📋 You don't have any tasks yet. Try adding one!"

        elif any(word in lower_message for word in ['complete', 'done', 'finish']) and any(word in lower_message for word in ['task', 'tasks']):
            tasks = await task_service.get_tasks(user_id)
            pending_tasks = [task for task in tasks if not task.completed]
            if pending_tasks:
                task_to_complete = pending_tasks[0]
                await task_service.update_task(user_id, task_to_complete.id, UpdateTaskInput(is_complete=True))
                response = f"✅ Successfully completed task: '{task_to_complete.title}'"
            else:
                response = "✅ All your tasks are already completed!"

        elif any(word in lower_message for word in ['delete', 'remove']) and any(word in lower_message for word in ['task', 'tasks']):
            tasks = await task_service.get_tasks(user_id)
            if tasks:
                task_to_delete = tasks[0]
                await task_service.delete_task(user_id, task_to_delete.id)
                response = f"🗑️ Successfully deleted task: '{task_to_delete.title}'"
            else:
                response = "❌ You don't have any tasks to delete."

        elif any(word in lower_message for word in ['update', 'edit']) and any(word in lower_message for word in ['task', 'tasks']):
            tasks = await task_service.get_tasks(user_id)
            if tasks:
                task_to_update = tasks[0]
                await task_service.update_task(user_id, task_to_update.id, UpdateTaskInput(title=f"{task_to_update.title} (Updated)"))
                response = f"✏️ Successfully updated task: '{task_to_update.title}'"
            else:
                response = "❌ You don't have any tasks to update."

        else:
            # Default AI response - run in a thread to avoid blocking the event loop
            import asyncio
            try:
                loop = asyncio.get_event_loop()

                # Run the OpenAI API call in a separate thread to avoid blocking
                response_obj = await loop.run_in_executor(
                    None,
                    lambda: openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful AI assistant for task management. Respond friendly and helpfully."},
                            {"role": "user", "content": message}
                        ],
                        max_tokens=150
                    )
                )
                response = response_obj.choices[0].message.content or f"I processed your request: {message}"
            except Exception:
                response = f"I received your message: '{message}'. You can ask me to add, list, complete, update, or delete tasks."

        # 4. Add AI response to conversation
        await self.add_message(
            conversation_id=conversation.id,
            sender=Sender.AI_AGENT,
            content=response
        )

        return response
