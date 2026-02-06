# backend/src/services/task_service.py
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.task import Task
from src.schemas.task import AddTaskInput, TaskOutput, UpdateTaskInput


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def verify_task_ownership(self, user_id: UUID, task_id: UUID) -> Optional[Task]:
        """
        Verifies if a task belongs to a specific user.
        """
        result = await self.session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.first()

    async def create_task(self, user_id: UUID, task_input: AddTaskInput) -> TaskOutput:
        """
        Creates a new task for a given user.
        """
        new_task = Task(
            user_id=user_id,
            title=task_input.title,
            description=task_input.description,
            due_date=task_input.due_date,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self.session.add(new_task)
        await self.session.flush()
        return TaskOutput(
            id=new_task.id,
            title=new_task.title,
            description=new_task.description,
            is_complete=new_task.is_complete,
        )

    async def get_tasks(self, user_id: UUID, is_complete: Optional[bool] = None) -> List[TaskOutput]:
        """
        Retrieves all tasks for a user, optionally filtered by completion status.
        """
        query = select(Task).where(Task.user_id == user_id)
        if is_complete is not None:
            query = query.where(Task.is_complete == is_complete)
        result = await self.session.exec(query)
        tasks = result.all()
        return [
            TaskOutput(
                id=task.id,
                title=task.title,
                description=task.description,
                is_complete=task.is_complete,
            )
            for task in tasks
        ]

    async def update_task(self, user_id: UUID, task_input: UpdateTaskInput) -> Optional[TaskOutput]:
        """
        Updates an existing task after verifying ownership.
        """
        task = await self.verify_task_ownership(user_id, task_input.task_id)
        if not task:
            return None

        if task_input.title is not None:
            task.title = task_input.title
        if task_input.description is not None:
            task.description = task_input.description
        if task_input.due_date is not None:
            task.due_date = task_input.due_date
        if task_input.is_complete is not None:
            task.is_complete = task_input.is_complete

        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        await self.session.flush()

        return TaskOutput(
            id=task.id,
            title=task.title,
            description=task.description,
            is_complete=task.is_complete,
        )

    async def complete_task(self, user_id: UUID, task_id: UUID) -> bool:
        """
        Marks a task as complete after verifying ownership.
        """
        task = await self.verify_task_ownership(user_id, task_id)
        if not task:
            return False

        task.is_complete = True
        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        await self.session.flush()
        return True

    async def delete_task(self, user_id: UUID, task_id: UUID) -> bool:
        """
        Deletes a task after verifying ownership.
        """
        task = await self.verify_task_ownership(user_id, task_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.flush()
        return True
