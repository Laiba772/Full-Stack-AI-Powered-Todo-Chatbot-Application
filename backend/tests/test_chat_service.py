import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.services.chat_service import ChatService
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message, Sender

@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def chat_service(mock_session):
    return ChatService(mock_session)

@pytest.fixture
def mock_user():
    return User(id=uuid4(), username="testuser", email="test@example.com", password_hash="hashed_password")

@pytest.fixture
def mock_conversation(mock_user):
    return Conversation(id=uuid4(), user_id=mock_user.id, title="Test Conversation")

@pytest.fixture
def mock_message(mock_conversation):
    return Message(conversation_id=mock_conversation.id, sender=Sender.USER, content="Hello AI!")

class TestChatService:

    @pytest.mark.asyncio
    async def test_create_conversation(self, chat_service, mock_user):
        user_id = mock_user.id
        title = "New Conversation"
        
        # Mock session.exec() to return an empty result initially for refreshing
        chat_service.session.exec.return_value.first.return_value = None 

        conversation = await chat_service.create_conversation(user_id, title)

        chat_service.session.add.assert_called_once()
        chat_service.session.commit.assert_called_once()
        chat_service.session.refresh.assert_called_once_with(conversation)
        assert conversation.user_id == user_id
        assert conversation.title == title
        assert isinstance(conversation.id, UUID)

    @pytest.mark.asyncio
    async def test_get_conversation(self, chat_service, mock_conversation):
        # Mock the exec().first() call
        mock_exec_result = MagicMock()
        mock_exec_result.first.return_value = mock_conversation
        chat_service.session.exec.return_value = mock_exec_result

        conversation = await chat_service.get_conversation(mock_conversation.id)

        chat_service.session.exec.assert_called_once()
        assert conversation == mock_conversation

    @pytest.mark.asyncio
    async def test_get_messages(self, chat_service, mock_conversation, mock_message):
        messages = [mock_message]
        # Mock the exec().all() call
        mock_exec_result = MagicMock()
        mock_exec_result.all.return_value = messages
        chat_service.session.exec.return_value = mock_exec_result

        retrieved_messages = await chat_service.get_messages(mock_conversation.id)

        chat_service.session.exec.assert_called_once()
        assert retrieved_messages == messages

    @pytest.mark.asyncio
    async def test_add_message(self, chat_service, mock_conversation):
        # Mock get_conversation to return the mock_conversation
        chat_service.get_conversation = AsyncMock(return_value=mock_conversation)

        sender = Sender.USER
        content = "Test message content"
        
        message = await chat_service.add_message(mock_conversation.id, sender, content)

        calls = [call(message), call(mock_conversation)]
        chat_service.session.add.assert_has_calls(calls, any_order=True)
        chat_service.session.commit.assert_called_once()
        refresh_calls = [call(message), call(mock_conversation)]
        chat_service.session.refresh.assert_has_calls(refresh_calls, any_order=True)

        assert message.conversation_id == mock_conversation.id
        assert message.sender == sender
        assert message.content == content
        assert mock_conversation.updated_at is not None
        assert isinstance(message.id, UUID)

    @pytest.mark.asyncio
    async def test_add_message_with_tool_info(self, chat_service, mock_conversation):
        # Mock get_conversation to return the mock_conversation
        chat_service.get_conversation = AsyncMock(return_value=mock_conversation)

        sender = Sender.AI_AGENT
        content = "Tool executed."
        tool_calls = [{"id": "call_1", "function": {"name": "tool", "arguments": "{}"}}]
        tool_output = [{"tool_call_id": "call_1", "name": "tool", "content": "Tool result"}]
        
        message = await chat_service.add_message(
            mock_conversation.id, sender, content, tool_calls=tool_calls, tool_output=tool_output
        )

        chat_service.session.assert_has_calls([
            call.add(message),
            call.refresh(message)
        ])
        chat_service.session.commit.assert_called_once()
        assert message.tool_calls == tool_calls
        assert message.tool_output == tool_output
        assert mock_conversation.updated_at is not None