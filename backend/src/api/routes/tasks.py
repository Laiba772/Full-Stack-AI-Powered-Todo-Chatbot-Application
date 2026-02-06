from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Optional
from datetime import datetime, timezone

from src.models.database import get_async_session
from src.models.task import Task
from src.models.user import User
from src.services.auth_service import get_current_user_from_betterauth
from src.schemas.task import (
    AddTaskInput,
    TaskOutput,
    UpdateTaskInput,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


# =========================
# Service Layer
# =========================
class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, user_id: UUID, task_data: AddTaskInput) -> Task:
        new_task = Task(**task_data.model_dump(), user_id=user_id)
        # Ensure UTC for due_date
        if new_task.due_date and new_task.due_date.tzinfo is not None:
            new_task.due_date = new_task.due_date.astimezone(timezone.utc).replace(tzinfo=None)
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task

    async def get_tasks(self, user_id: UUID, page: int = 1, page_size: int = 20) -> List[Task]:
        offset = (page - 1) * page_size
        stmt = (
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        tasks = (await self.db.exec(stmt)).all()
        return tasks

    async def get_task(self, user_id: UUID, task_id: UUID) -> Task:
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = (await self.db.exec(stmt)).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def update_task(self, user_id: UUID, task_id: UUID, task_data: UpdateTaskInput) -> Task:
        task = await self.get_task(user_id, task_id)
        for field, value in task_data.model_dump(exclude_unset=True).items():
            if field == "due_date" and value and value.tzinfo is not None:
                value = value.astimezone(timezone.utc).replace(tzinfo=None)
            setattr(task, field, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, user_id: UUID, task_id: UUID) -> None:
        task = await self.get_task(user_id, task_id)
        await self.db.delete(task)
        await self.db.commit()


# Dependency
async def get_task_service(db: AsyncSession = Depends(get_async_session)) -> TaskService:
    return TaskService(db)


# =========================
# Routes
# =========================

def verify_user_access(user: User):
    """Ensure users can only access their own tasks."""
    # This function just validates that the user is authenticated
    # and can access their own resources. Simply returning the user
    # is sufficient for the dependency system.
    return user


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    task_data: AddTaskInput,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user_from_betterauth),
):
    verify_user_access(user)
    task = await service.create_task(user.id, task_data)
    return TaskOutput.model_validate(task)


@router.get("")
async def list_tasks_endpoint(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user_from_betterauth),
):
    verify_user_access(user)
    tasks = await service.get_tasks(user.id, page, page_size)
    return {
        "tasks": [TaskOutput.model_validate(t) for t in tasks],
        "page": page
    }


@router.get("/{task_id}")
async def get_task_endpoint(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user_from_betterauth),
):
    verify_user_access(user)
    task = await service.get_task(user.id, task_id)
    return TaskOutput.model_validate(task)


@router.patch("/{task_id}")
async def update_task_endpoint(
    task_id: UUID,
    task_data: UpdateTaskInput,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user_from_betterauth),
):
    verify_user_access(user)
    task = await service.update_task(user.id, task_id, task_data)
    return TaskOutput.model_validate(task)


@router.patch("/{task_id}/complete")
async def complete_task_endpoint(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user_from_betterauth),
):
    verify_user_access(user)
    task = await service.update_task(user.id, task_id, UpdateTaskInput(is_complete=True))
    return TaskOutput.model_validate(task)


@router.patch("/{task_id}/incomplete")
async def incomplete_task_endpoint(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user_from_betterauth),
):
    verify_user_access(user)
    task = await service.update_task(user.id, task_id, UpdateTaskInput(is_complete=False))
    return TaskOutput.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user_from_betterauth),
):
    verify_user_access(user)
    await service.delete_task(user.id, task_id)
