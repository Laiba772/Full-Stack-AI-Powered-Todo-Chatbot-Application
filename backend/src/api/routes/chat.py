from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from openai import OpenAI

from src.services.chat_service import ChatService
from src.api.routes.tasks import TaskService
from src.models.database import get_async_session

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(
    user_id: UUID,
    message: str,
    session: AsyncSession = Depends(get_async_session)
):
    chat_service = ChatService(session)
    task_service = TaskService(session)
    openai_client = OpenAI(api_key="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")  # Set your key

    response = await chat_service.handle_message(
        user_id=user_id,
        message=message,
        task_service=task_service,
        openai_client=openai_client
    )
    return {"response": response}
