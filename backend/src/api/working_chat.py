# backend/src/api/working_chat.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timezone
import re
from sqlmodel import select

from src.models.database import get_async_session
from src.models.conversation import Conversation
from src.models.message import Message, Sender
from src.api.routes.tasks import TaskService, get_task_service
from src.api.dependencies.auth import get_current_user, TokenUser
from src.schemas.task import AddTaskInput, UpdateTaskInput

router = APIRouter()


# Request model for the chat endpoint
class ChatMessageRequest(BaseModel):
    message: str

# Response model for the chat endpoint
class ChatMessageResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatMessageResponse)
async def chat_endpoint(
    chat_message_request: ChatMessageRequest,
    current_user: TokenUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    task_service: TaskService = Depends(get_task_service)
):
    user_id = current_user.user_id

    # --- Get the latest conversation for the user ---
    query = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
    result = await session.exec(query)
    conversation = result.first()

    if not conversation:
        conversation = Conversation(user_id=user_id, title="New Chat")
        session.add(conversation)
        try:
            await session.commit()
            await session.refresh(conversation)
        except:
            await session.rollback()
            raise

    conversation_id = conversation.id

    # --- Add user message ---
    user_message = Message(
        conversation_id=conversation_id,
        sender=Sender.USER,
        content=chat_message_request.message
    )
    session.add(user_message)
    try:
        await session.commit()
        await session.refresh(user_message)
    except:
        await session.rollback()
        raise

    # --- Determine AI response ---
    lower_message = chat_message_request.message.lower()
    response = ""

    try:
        # Add Task
        if any(word in lower_message for word in ['add', 'create', 'new']) and any(word in lower_message for word in ['task', 'todo']):
            import re
            task_match = re.search(r'(?:add|create|new)\s+(?:a\s+)?(.+)', chat_message_request.message, re.IGNORECASE)
            task_title = task_match.group(1).strip() if task_match else "New task"
            task_input = AddTaskInput(title=task_title, description=f"Created via AI assistant: {chat_message_request.message}")
            created_task = await task_service.create_task(user_id, task_input)
            response = f"✅ Successfully added task: '{created_task.title}'"

        # List Tasks
        elif any(word in lower_message for word in ['list', 'show', 'my', 'all']) and any(word in lower_message for word in ['task', 'tasks', 'todo']):
            tasks = await task_service.get_tasks(user_id)
            if tasks:
                task_list = "\n".join([f"• {task.title} ({'✓ Completed' if task.is_complete else '○ Pending'})" for task in tasks])
                response = f"📋 Your Tasks:\n{task_list}"
            else:
                response = "📋 You don't have any tasks yet. Try adding one!"

        # Complete Task
        elif any(word in lower_message for word in ['complete', 'done', 'finish']) and any(word in lower_message for word in ['task', 'tasks']):
            tasks = await task_service.get_tasks(user_id)
            pending_tasks = [task for task in tasks if not task.is_complete]
            if pending_tasks:
                task_to_complete = pending_tasks[0]
                await task_service.update_task(user_id, UpdateTaskInput(task_id=task_to_complete.id, is_complete=True))
                response = f"✅ Successfully completed task: '{task_to_complete.title}'"
            else:
                response = "✅ All your tasks are already completed!"

        # Delete Task
        elif any(word in lower_message for word in ['delete', 'remove']) and any(word in lower_message for word in ['task', 'tasks']):
            tasks = await task_service.get_tasks(user_id)
            if tasks:
                task_to_delete = tasks[0]
                await task_service.delete_task(user_id, task_to_delete.id)
                response = f"🗑️ Successfully deleted task: '{task_to_delete.title}'"
            else:
                response = "❌ You don't have any tasks to delete."

        # Update Task
        elif any(word in lower_message for word in ['update', 'edit']) and any(word in lower_message for word in ['task', 'tasks']):
            tasks = await task_service.get_tasks(user_id)
            if tasks:
                task_to_update = tasks[0]
                await task_service.update_task(user_id, UpdateTaskInput(task_id=task_to_update.id, title=f"{task_to_update.title} (Updated)"))
                response = f"✏️ Successfully updated task: '{task_to_update.title}'"
            else:
                response = "❌ You don't have any tasks to update."

        # Default AI response
        else:
            response = f"I received your message: '{chat_message_request.message}'. You can ask me to add, list, complete, update, or delete tasks."

    except Exception as e:
        response = f"❌ Sorry, I couldn't process your request. Error: {str(e)}"

    # --- Add AI response to conversation ---
    ai_message = Message(
        conversation_id=conversation_id,
        sender=Sender.AI_AGENT,
        content=response
    )
    session.add(ai_message)

    # Update conversation timestamp
    conversation.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(conversation)

    # Commit all changes
    try:
        await session.commit()
    except:
        await session.rollback()

    return ChatMessageResponse(response=response)
