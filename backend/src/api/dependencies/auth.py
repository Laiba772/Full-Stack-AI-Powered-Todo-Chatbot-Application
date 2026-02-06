"""Authentication dependencies for FastAPI with BetterAuth compatibility."""
from typing import Optional
from uuid import UUID
from fastapi import Request, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession # Import AsyncSession

from src.models.user import User
from src.models.database import get_async_session # Use get_async_session
from src.services.auth_service import get_current_user_from_betterauth, get_optional_user_from_betterauth


class AuthenticationError(HTTPException):
    """Raised when authentication fails."""

    def __init__(self, message: str, code: str = "UNAUTHORIZED"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": code,
                "message": message,
                "details": None,
            },
        )


class TokenUser(BaseModel):
    """User information extracted from JWT token."""

    user_id: UUID
    email: str

    @classmethod
    def from_user_model(cls, user: User) -> "TokenUser":
        """Create TokenUser from User model."""
        return cls(
            user_id=user.id,
            email=user.email,
        )


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session), # Use AsyncSession and get_async_session
) -> TokenUser:
    """Dependency to extract and verify the current user from BetterAuth session.

    Args:
        request: FastAPI request object containing session information

    Returns:
        TokenUser with user_id and email from session

    Raises:
        AuthenticationError: If session is missing, invalid, or expired
    """
    try:
        # Get user from BetterAuth-compatible session
        user = await get_current_user_from_betterauth(request, session)

        # Convert to TokenUser
        return TokenUser.from_user_model(user)
    except HTTPException as e:
        # Propagate the specific HTTPException details
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )


async def get_optional_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session), # Use AsyncSession and get_async_session
) -> Optional[TokenUser]:
    """Dependency to optionally extract user from BetterAuth session.

    Unlike get_current_user, this returns None instead of raising
    an exception when no valid session is provided.

    Args:
        request: FastAPI request object containing session information

    Returns:
        TokenUser if valid session provided, None otherwise
    """
    try:
        user = await get_optional_user_from_betterauth(request, session) # Await get_optional_user_from_betterauth
        if user:
            return TokenUser.from_user_model(user)
        return None
    except HTTPException:
        return None


def require_auth(
    current_user: TokenUser = Depends(get_current_user),
) -> TokenUser:
    """Explicit auth dependency for routes that require authentication.

    This is an alias for get_current_user that makes the intent clearer
    in route definitions.
    """
    return current_user


def verify_user_access(user_id: UUID, current_user: TokenUser = Depends(get_current_user)):
    """Dependency to verify that the path user_id matches the authenticated user."""
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "Access denied"},
        )
    return current_user


from fastapi import Request
import re
from uuid import UUID

def verify_user_from_path(request: Request, current_user: TokenUser = Depends(get_current_user)):
    """Extract user_id from path and verify it matches the authenticated user."""
    # Extract user_id from the request path
    path = request.url.path
    # Look for UUID pattern in the path after /api/users/ or just /api/
    # Support both patterns: /api/{user_id}/... and /api/users/{user_id}/...
    match = re.search(r'/api/(?:users/)?([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})', path)

    if not match:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "Could not extract user ID from path"},
        )

    path_user_id = UUID(match.group(1))

    if current_user.user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "Access denied"},
        )

    return current_user

