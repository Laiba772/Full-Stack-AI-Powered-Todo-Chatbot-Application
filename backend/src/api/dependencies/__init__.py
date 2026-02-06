# API dependencies package
from .auth import (
    get_optional_user,
    require_auth,
    verify_user_access,
    TokenUser,
    AuthenticationError,
    verify_user_from_path
)



__all__ = [
    "get_current_user",
    "get_optional_user",
    "require_auth",
    "verify_user_access",
    "verify_user_id",
    "verify_user_from_path",
    "TokenUser",
    "AuthenticationError",
    "get_ai_agent_service"
]
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from src.core.security import decode_token
from src.models.database import get_async_session
from src.models.user import User
from sqlmodel import select
from uuid import UUID

from src.services.chat_service import ChatService
from src.services.ai_agent_service import AIAgentService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Assuming a token endpoint at /token, adjust if needed

async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to get the current authenticated user.

    Args:
        session: An asynchronous database session.
        token: The JWT token from the Authorization header.

    Returns:
        The authenticated User object.

    Raises:
        HTTPException: If the token is invalid, expired, or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = await session.exec(select(User).where(User.id == UUID(user_id)))
        current_user = user.first()
        if current_user is None:
            raise credentials_exception
        return current_user
    except HTTPException:
        raise
    except Exception:
        raise credentials_exception

from fastapi import Request
import re

def verify_user_id(
    request: Request,
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to verify if the user ID from the path matches the authenticated user's ID.

    Args:
        request: The FastAPI request object to extract path parameters.
        current_user: The authenticated user obtained from `get_current_user` dependency.

    Returns:
        The authenticated User object if the IDs match.

    Raises:
        HTTPException: If the user IDs do not match (403 Forbidden).
    """
    # Extract user_id from the request path
    path = request.url.path
    # Look for UUID pattern in the path after /api/ or /api/users/
    match = re.search(r'/api/(?:users/)?([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})', path)

    if not match:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not extract user ID from path",
        )

    path_user_id = UUID(match.group(1))

    if path_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's resources",
        )
    return current_user

def get_chat_service(session: AsyncSession = Depends(get_async_session)) -> ChatService:
    """
    Dependency to get a ChatService instance.
    """
    return ChatService(session)

def get_ai_agent_service(session: AsyncSession = Depends(get_async_session)) -> AIAgentService:
    """
    Dependency to get an AIAgentService instance.
    """
    return AIAgentService(session)