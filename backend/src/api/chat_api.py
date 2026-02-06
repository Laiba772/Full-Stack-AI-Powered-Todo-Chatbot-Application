from typing import Optional, List, Dict
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message, Sender # Import Sender
from src.services.chat_service import ChatService
from src.services.ai_agent_service import AIAgentService # Import AIAgentService
from src.api.dependencies import get_current_user, verify_user_id, get_chat_service, get_ai_agent_service # Import new dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.database import get_async_session

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

class ChatResponse(BaseModel):
    conversation_id: UUID
    message: str
    ai_message: str
    tool_invoked: bool = False # New field for T041

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(verify_user_id),
    chat_service: ChatService = Depends(get_chat_service),
    ai_agent_service: AIAgentService = Depends(get_ai_agent_service)
):
    """
    Handles chat messages from the user and returns an AI response.
    """
    conversation: Optional[Conversation] = None

    if request.conversation_id:
        conversation = await chat_service.get_conversation(request.conversation_id)
        if not conversation or conversation.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or not authorized."
            )
    else:
        conversation = await chat_service.create_conversation(current_user.id)

    # Add user message to conversation
    await chat_service.add_message(conversation.id, Sender.USER, request.message)

    # Get conversation history for AI agent
    messages = await chat_service.get_messages(conversation.id)

    # Generate AI response
    ai_response_content, tool_calls, tool_output = await ai_agent_service.generate_response( # Unpack new return type
        user=current_user,
        conversation=conversation,
        messages=messages,
        user_message=request.message
    )

    # Add AI response to conversation, including tool calls and outputs if any
    await chat_service.add_message(
        conversation.id,
        Sender.AI_AGENT,
        ai_response_content,
        tool_calls=tool_calls, # Pass tool_calls
        tool_output=tool_output # Pass tool_output
    )

    return ChatResponse(
        conversation_id=conversation.id,
        message=request.message,
        ai_message=ai_response_content,
        tool_invoked=bool(tool_calls) # Set based on whether tool_calls were made
    )