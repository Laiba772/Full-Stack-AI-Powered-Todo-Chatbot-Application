"""
BetterAuth-compatible authentication service for FastAPI backend.
This service integrates with BetterAuth frontend by validating
session cookies and providing user context.
"""

from typing import Optional
from fastapi import Request, HTTPException, status, Depends
from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.user import User
from src.models.database import get_async_session

from datetime import datetime, timedelta, timezone
import os
from uuid import UUID

from jose import JWTError, jwt, ExpiredSignatureError
import bcrypt


class TokenData(BaseModel):
    user_id: str
    email: str
    exp: int


class BetterAuthIntegration:
    def __init__(self):
        self.secret = os.getenv("JWT_SECRET", "fallback_secret_key_for_dev")
        self.algorithm = "HS256"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        if len(plain_password.encode("utf-8")) > 72:
            plain_password = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def get_password_hash(self, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": int(expire.timestamp())})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Optional[TokenData]:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            exp: int = payload.get("exp")

            if not user_id or not email or not exp:
                return None

            return TokenData(user_id=user_id, email=email, exp=exp)

        except ExpiredSignatureError:
            # Let caller handle TOKEN_EXPIRED specifically
            raise

        except JWTError:
            return None


auth_service = BetterAuthIntegration()


class UserSession(BaseModel):
    user_id: str
    email: str
    expires_at: datetime


async def get_current_user_from_betterauth(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
) -> User:

    auth_cookie = request.cookies.get("access_token") or request.headers.get("Authorization")

    if not auth_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "NOT_AUTHENTICATED", "message": "Not authenticated", "details": None},
        )

    if auth_cookie.startswith("Bearer "):
        auth_cookie = auth_cookie[7:]

    print(f"DEBUG: auth_cookie received: {auth_cookie}") # Debugging line

    try:
        token_data = auth_service.decode_token(auth_cookie)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "TOKEN_EXPIRED", "message": "Token has expired", "details": None},
        )

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Could not validate credentials", "details": None},
        )

    user = (
        await session.exec(select(User).where(User.id == UUID(token_data.user_id)))
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "USER_NOT_FOUND", "message": "User not found", "details": None},
        )

    return user


async def get_optional_user_from_betterauth(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
) -> Optional[User]:
    try:
        return await get_current_user_from_betterauth(request, session)
    except HTTPException:
        return None
