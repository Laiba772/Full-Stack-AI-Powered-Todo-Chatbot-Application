from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel, JSON, Column
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from src.models.conversation import Conversation

class Sender(str, Enum):
    USER = "user"
    AI_AGENT = "ai_agent"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    sender: Sender
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    tool_output: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
