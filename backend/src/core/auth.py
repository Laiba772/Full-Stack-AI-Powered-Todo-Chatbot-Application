from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from uuid import UUID
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.config import settings


# =========================
# Custom Errors
# =========================

class InvalidTokenError(Exception):
    pass


class ExpiredTokenError(Exception):
    pass


# =========================
# JWT Functions
# =========================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def create_jwt_token(
    user_id: UUID,
    email: str,
    secret: str = settings.jwt_secret,
    expiration_minutes: int = settings.jwt_expiration_minutes,
    algorithm: str = settings.jwt_algorithm,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expiration_minutes)).timestamp()),
        "iss": "todo-app",
    }

    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token


def verify_jwt_token(token: str, secret: str = settings.jwt_secret, algorithms=[settings.jwt_algorithm]) -> Dict[str, Any]:
    if not token:
        raise InvalidTokenError("Token is empty")

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=algorithms,
            options={"require": ["exp", "iat", "sub"]},
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError("Token has expired")

    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token")


def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    Decode token WITHOUT verifying signature.
    Used only for frontend / debug / non-secure reads.
    """
    try:
        payload = jwt.decode(
            token,
            options={"verify_signature": False},
        )
        return payload
    except Exception:
        return {}


async def get_current_user_id_from_token(token: str = Depends(oauth2_scheme)) -> UUID:
    """
    FastAPI dependency to validate JWT token and return the current user's ID.
    Raises HTTPException if the token is invalid or expired.
    """
    try:
        payload = verify_jwt_token(token)
        user_id = UUID(payload["sub"])
        return user_id
    except ExpiredTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token validation",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

