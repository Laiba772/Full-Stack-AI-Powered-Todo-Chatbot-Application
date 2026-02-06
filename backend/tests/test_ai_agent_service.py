import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from sqlmodel.ext.asyncio.session import AsyncSession
from src.services.ai_agent_service import AIAgentService
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message, Sender
from src.config import settings
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall, ChatCompletionChunk
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_chunk import ChoiceDelta

# Mock settings for testing
@pytest.fixture(autouse=True)
def mock_settings():
    with patch('src.config.settings') as mock:
        mock.openai_api_key = "test_api_key"
        mock.openai_agent_model = "test_model"
        mock.openai_agent_max_tokens = 100
        mock.ai_agent_system_prompt = "Test system prompt."
        yield mock

@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def ai_agent_service(mock_session):
    return AIAgentService(mock_session)

@pytest.fixture
def mock_user():
    return User(id=uuid4(), username="testuser", email="test@example.com", password_hash="hashed_password")

@pytest.fixture
def mock_conversation(mock_user):
    return Conversation(id=uuid4(), user_id=mock_user.id)

@pytest.fixture
def mock_messages():
    return [
        Message(conversation_id=uuid4(), sender=Sender.USER, content="Hello"),
        Message(conversation_id=uuid4(), sender=Sender.AI_AGENT, content="Hi there!")
    ]

class TestAIAgentService:

    @pytest.mark.asyncio
    async def test_generate_response_text_only(self, ai_agent_service, mock_user, mock_conversation, mock_messages):
        mock_openai_response = MagicMock()
        mock_openai_response.choices = [
            Choice(
                index=0,
                message=ChatCompletionMessage(role="assistant", content="AI text response."),
                finish_reason="stop",
                logprobs=None
            )
        ]

        with patch('openai.OpenAI', MagicMock(return_value=MagicMock(chat=MagicMock(completions=MagicMock(create=AsyncMock(return_value=mock_openai_response)))))):
            ai_response_content, tool_calls, tool_output = await ai_agent_service.generate_response(
                mock_user, mock_conversation, mock_messages, "User's new message"
            )

            assert ai_response_content == "AI text response."
            assert tool_calls is None
            assert tool_output is None

    @pytest.mark.asyncio
    async def test_generate_response_with_tool_call(self, ai_agent_service, mock_user, mock_conversation, mock_messages):
        # Mock a tool call response from OpenAI
        mock_tool_call = ChatCompletionMessageToolCall(
            id="call_123",
            function=MagicMock(name="echo_tool", arguments='{"text": "test_input"}'),
            type="function"
        )
        mock_openai_response_tool_call = MagicMock()
        mock_openai_response_tool_call.choices = [
            Choice(
                index=0,
                message=ChatCompletionMessage(role="assistant", tool_calls=[mock_tool_call]),
                finish_reason="tool_calls",
                logprobs=None
            )
        ]

        # Mock the tool's return value
        mock_tool_instance = MagicMock()
        mock_tool_instance.run = AsyncMock(return_value={"echoed_text": "test_input"})

        # Mock the second OpenAI response after tool execution
        mock_openai_response_final = MagicMock()
        mock_openai_response_final.choices = [
            Choice(
                index=0,
                message=ChatCompletionMessage(role="assistant", content="Tool executed response."),
                finish_reason="stop",
                logprobs=None
            )
        ]

        with patch('openai.OpenAI', MagicMock(return_value=MagicMock(chat=MagicMock(completions=MagicMock(create=AsyncMock(side_effect=[mock_openai_response_tool_call, mock_openai_response_final])))))) as mock_openai, patch('src.services.tool_registry.ToolRegistry._tools', {"echo_tool": MagicMock(return_value=mock_tool_instance)}) as mock_registry:
            
            ai_response_content, tool_calls, tool_output = await ai_agent_service.generate_response(
                mock_user, mock_conversation, mock_messages, "Echo 'test_input'"
            )

            assert ai_response_content == "Tool executed response."
            assert tool_calls is not None
            assert len(tool_calls) == 1
            assert tool_calls[0]["function"]["name"] == "echo_tool"
            assert tool_output is not None
            assert len(tool_output) == 1
            assert tool_output[0]["content"] == "{'echoed_text': 'test_input'}"
