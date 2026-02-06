from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.message import Message

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")
