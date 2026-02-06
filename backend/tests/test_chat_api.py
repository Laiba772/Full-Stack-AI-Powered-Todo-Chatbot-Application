import pytest
from httpx import AsyncClient
from uuid import uuid4, UUID
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException

from src.main import app
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message, Sender
from src.services.chat_service import ChatService
from src.api.chat import get_chat_service
from src.services.ai_agent_service import AIAgentService
from src.api.dependencies import get_current_user, verify_user_id 
from src.api.dependencies import get_ai_agent_service

# Fixtures
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_user():
    return User(id=uuid4(), username="testuser", email="test@example.com", password_hash="hashed_password")

@pytest.fixture
def mock_conversation(mock_user):
    return Conversation(id=uuid4(), user_id=mock_user.id, title="Test Conversation")

@pytest.fixture
def mock_chat_service():
    service = AsyncMock(spec=ChatService)
    service.get_conversation.return_value = None
    service.create_conversation.return_value = Conversation(id=uuid4(), user_id=uuid4())
    service.add_message.return_value = Message(conversation_id=uuid4(), sender=Sender.USER, content="mock message")
    service.get_messages.return_value = []
    return service

@pytest.fixture
def mock_ai_agent_service():
    service = AsyncMock(spec=AIAgentService)
    service.generate_response.return_value = ("AI response content", None, None)
    return service

# Overrides for dependencies
def override_get_current_user(mock_user: User):
    async def _override():
        return mock_user
    return _override

def override_verify_user_id(mock_user: User):
    def _override(path_user_id: UUID, current_user: User = Depends(get_current_user)):
        if path_user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        return current_user
    return _override

def override_get_chat_service(mock_chat_service: ChatService):
    def _override():
        return mock_chat_service
    return _override

def override_get_ai_agent_service(mock_ai_agent_service: AIAgentService):
    def _override():
        return mock_ai_agent_service
    return _override

# Apply overrides globally for tests
app.dependency_overrides[get_current_user] = override_get_current_user(User(id=uuid4(), username="default", email="default@example.com", password_hash="hashed"))
app.dependency_overrides[verify_user_id] = override_verify_user_id(User(id=uuid4(), username="default", email="default@example.com", password_hash="hashed"))
app.dependency_overrides[get_chat_service] = override_get_chat_service(AsyncMock(spec=ChatService))
app.dependency_overrides[get_ai_agent_service] = override_get_ai_agent_service(AsyncMock(spec=AIAgentService))


class TestChatAPI:

    @pytest.mark.asyncio
    async def test_chat_new_conversation(
        self, client: AsyncClient, mock_user: User, mock_chat_service: ChatService, mock_ai_agent_service: AIAgentService
    ):
        # Override specific dependencies for this test
        app.dependency_overrides[get_current_user] = override_get_current_user(mock_user)
        app.dependency_overrides[verify_user_id] = override_verify_user_id(mock_user)
        app.dependency_overrides[get_chat_service] = override_get_chat_service(mock_chat_service)
        app.dependency_overrides[get_ai_agent_service] = override_get_ai_agent_service(mock_ai_agent_service)

        mock_conversation_id = uuid4()
        mock_chat_service.create_conversation.return_value = Conversation(id=mock_conversation_id, user_id=mock_user.id)
        mock_ai_agent_service.generate_response.return_value = ("Hello from AI!", None, None)

        response = client.post(
            f"/api/{mock_user.id}/chat",
            json={"message": "Hi AI!"}
        )

        assert response.status_code == 200
        assert response.json()["ai_message"] == "Hello from AI!"
        assert response.json()["conversation_id"] == str(mock_conversation_id)
        assert mock_chat_service.create_conversation.called
        assert mock_chat_service.add_message.call_count == 2 # User and AI message
        assert mock_ai_agent_service.generate_response.called
        assert response.json()["tool_invoked"] is False
        
        # Reset overrides
        app.dependency_overrides = {}

    @pytest.mark.asyncio
    async def test_chat_existing_conversation(
        self, client: AsyncClient, mock_user: User, mock_conversation: Conversation,
        mock_chat_service: ChatService, mock_ai_agent_service: AIAgentService
    ):
        # Override specific dependencies for this test
        app.dependency_overrides[get_current_user] = override_get_current_user(mock_user)
        app.dependency_overrides[verify_user_id] = override_verify_user_id(mock_user)
        app.dependency_overrides[get_chat_service] = override_get_chat_service(mock_chat_service)
        app.dependency_overrides[get_ai_agent_service] = override_get_ai_agent_service(mock_ai_agent_service)

        mock_chat_service.get_conversation.return_value = mock_conversation
        mock_ai_agent_service.generate_response.return_value = ("Continuing conversation", None, None)

        response = client.post(
            f"/api/{mock_user.id}/chat",
            json={"message": "Another message", "conversation_id": str(mock_conversation.id)}
        )

        assert response.status_code == 200
        assert response.json()["ai_message"] == "Continuing conversation"
        assert response.json()["conversation_id"] == str(mock_conversation.id)
        assert mock_chat_service.get_conversation.called_once_with(mock_conversation.id)
        assert mock_chat_service.add_message.call_count == 2
        assert mock_ai_agent_service.generate_response.called
        assert response.json()["tool_invoked"] is False

        # Reset overrides
        app.dependency_overrides = {}

    @pytest.mark.asyncio
    async def test_chat_unauthorized_user(self, client: AsyncClient, mock_user: User):
        # Use a different user for verification than the one in the path
        unauthorized_user = User(id=uuid4(), username="unauth", email="unauth@example.com", password_hash="hashed")
        app.dependency_overrides[get_current_user] = override_get_current_user(unauthorized_user)
        app.dependency_overrides[verify_user_id] = override_verify_user_id(unauthorized_user) # Ensure verify_user_id also gets the unauthorized user

        response = client.post(
            json={"message": "Should be unauthorized"}
        )

        assert response.status_code == 403
        assert "Not authorized" in response.json()["detail"]

        # Reset overrides
        app.dependency_overrides = {}

    @pytest.mark.asyncio
    async def test_chat_with_tool_invocation(
        self, client: AsyncClient, mock_user: User, mock_conversation: Conversation,
        mock_chat_service: ChatService, mock_ai_agent_service: AIAgentService
    ):
        app.dependency_overrides[get_current_user] = override_get_current_user(mock_user)
        app.dependency_overrides[verify_user_id] = override_verify_user_id(mock_user)
        app.dependency_overrides[get_chat_service] = override_get_chat_service(mock_chat_service)
        app.dependency_overrides[get_ai_agent_service] = override_get_ai_agent_service(mock_ai_agent_service)

        mock_tool_calls = [{"id": "call_abc", "function": {"name": "echo_tool", "arguments": '{"text": "test"}'}}]
        mock_tool_output = [{"tool_call_id": "call_abc", "name": "echo_tool", "content": "{'echoed_text': 'test'}"}]
        
        mock_ai_agent_service.generate_response.return_value = ("Tool output processed.", mock_tool_calls, mock_tool_output)

        response = client.post(
            f"/api/{mock_user.id}/chat",
            json={"message": "Echo 'test'"}
        )

        assert response.status_code == 200
        assert response.json()["ai_message"] == "Tool output processed."
        assert response.json()["tool_invoked"] is True
        mock_chat_service.add_message.assert_called_with(
            mock_conversation.id, Sender.AI_AGENT, "Tool output processed.",
            tool_calls=mock_tool_calls, tool_output=mock_tool_output
        )

        # Reset overrides
        app.dependency_overrides = {}