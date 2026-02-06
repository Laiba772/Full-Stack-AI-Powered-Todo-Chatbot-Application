from typing import Optional, List
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AddTaskInput(BaseModel):
    """Input schema for adding a new task."""
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskOutput(BaseModel):
    """Output schema for a task."""
    id: UUID
    title: str
    description: Optional[str] = None
    is_complete: bool

    class Config:
        from_attributes = True

class ListTasksOutput(BaseModel):
    """Output schema for listing tasks."""
    tasks: List[TaskOutput]
    page: int = 1

class UpdateTaskInput(BaseModel):
    """Input schema for updating an existing task."""
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_complete: Optional[bool] = Field(default=None, alias="is_completed")

    class Config:
        populate_by_name = True

class CompleteTaskInput(BaseModel):
    """Input schema for marking a task as complete."""
    task_id: UUID

class DeleteTaskInput(BaseModel):
    """Input schema for deleting a task."""
    task_id: UUID

class StatusOutput(BaseModel):
    """Output schema for status of an operation."""
    task_id: UUID
    status: str
