import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from sqlmodel import Session, select
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message, Sender
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.database import get_async_session


class TestModels:

    @pytest.mark.asyncio
    async def test_create_user(self, session: AsyncSession):
        user = User(username="testuser", email="test@example.com", password_hash="hashedpassword")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password_hash == "hashedpassword"
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    @pytest.mark.asyncio
    async def test_read_user(self, session: AsyncSession):
        user = User(username="readuser", email="read@example.com", password_hash="hashedpassword")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        result = await session.exec(select(User).where(User.id == user.id))
        retrieved_user = result.first()
        assert retrieved_user == user

    @pytest.mark.asyncio
    async def test_update_user(self, session: AsyncSession):
        user = User(username="updateuser", email="update@example.com", password_hash="hashedpassword")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        user.email = "updated@example.com"
        session.add(user)
        await session.commit()
        await session.refresh(user)

        result = await session.exec(select(User).where(User.id == user.id))
        updated_user = result.first()
        assert updated_user.email == "updated@example.com"

    @pytest.mark.asyncio
    async def test_delete_user(self, session: AsyncSession):
        user = User(username="deleteuser", email="delete@example.com", password_hash="hashedpassword")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        await session.delete(user)
        await session.commit()

        result = await session.exec(select(User).where(User.id == user.id))
        deleted_user = result.first()
        assert deleted_user is None

    @pytest.mark.asyncio
    async def test_create_conversation(self, session: AsyncSession):
        user = User(username="convuser", email="conv@example.com", password_hash="hashedpassword")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        conversation = Conversation(user_id=user.id, title="Test Conversation")
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        assert conversation.id is not None
        assert conversation.user_id == user.id
        assert conversation.title == "Test Conversation"

    @pytest.mark.asyncio
    async def test_read_conversation_with_user(self, session: AsyncSession):
        user = User(username="convreaduser", email="convread@example.com", password_hash="hashedpassword")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        conversation = Conversation(user_id=user.id, title="Read Conversation")
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        result = await session.exec(select(Conversation).where(Conversation.id == conversation.id))
        retrieved_conversation = result.first()
        assert retrieved_conversation == conversation
        # Test relationship
        assert retrieved_conversation.user.id == user.id

    @pytest.mark.asyncio
    async def test_create_message(self, session: AsyncSession):
        user = User(username="msguser", email="msg@example.com", password_hash="hashedpassword")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        conversation = Conversation(user_id=user.id, title="Message Conversation")
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        message = Message(conversation_id=conversation.id, sender=Sender.USER, content="Hello AI!")
        session.add(message)
        await session.commit()
        await session.refresh(message)

        assert message.id is not None
        assert message.conversation_id == conversation.id
        assert message.sender == Sender.USER
        assert message.content == "Hello AI!"

    @pytest.mark.asyncio
    async def test_read_message_with_conversation(self, session: AsyncSession):
        user = User(username="msgreaduser", email="msgread@example.com", password_hash="hashedpassword")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        conversation = Conversation(user_id=user.id, title="Read Message Conversation")
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        message = Message(conversation_id=conversation.id, sender=Sender.AI_AGENT, content="How can I help?")
        session.add(message)
        await session.commit()
        await session.refresh(message)

        result = await session.exec(select(Message).where(Message.id == message.id))
        retrieved_message = result.first()
        assert retrieved_message == message
        # Test relationship
        assert retrieved_message.conversation.id == conversation.id