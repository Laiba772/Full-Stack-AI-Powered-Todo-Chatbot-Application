from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship

# Import User for relationship definition
from src.models.user import User


class Task(SQLModel, table=True):
    """Task entity for todo items.

    Attributes:
        id: Unique task identifier (UUID)
        user_id: Foreign key to the User who owns this task
        title: The title of the task
        description: The main content of the todo task
        due_date: Optional timestamp for when the task is due
        is_complete: Indicates if the task is completed
        created_at: Timestamp of task creation
        updated_at: Timestamp of last update
        user: The User object associated with this task (relationship)
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(index=True)
    description: str = Field(index=True, max_length=255)
    due_date: Optional[datetime] = Field(default=None)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: Optional[User] = Relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return (
            f"<Task id={self.id} user_id={self.user_id} "
            f"description='{self.description[:20]}...' is_complete={self.is_complete}>"
        )