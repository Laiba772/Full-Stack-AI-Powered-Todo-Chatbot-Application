import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# backend/tests/conftest.py
pytest_plugins = ("pytest_asyncio",)
# backend/tests/conftest.py
"""Test configuration and fixtures."""
import os
import pytest
import asyncio
from datetime import timedelta
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.pool import StaticPool
from typing import AsyncGenerator
from uuid import uuid4, UUID

from src.main import app
from src.models.database import get_async_session, set_engine # Use get_async_session and set_engine
from src.models.task import Task
from src.models.user import User
from src.models.message import Message
from src.models.tool_invocation import ToolInvocation
from src.services.auth_service import auth_service
from src.config import get_settings, settings as global_app_settings # Import get_settings and the global settings instance

# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:" # Use aiosqlite for async



@pytest.fixture(name="session")
async def fixture_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session with explicit rollback after each test."""
    async with AsyncSession(engine, expire_on_commit=False) as session: # Add expire_on_commit=False here
        yield session  # Yield the session directly
        # Rollback all changes after the test is complete
        await session.rollback()

@pytest.fixture(name="engine", scope="function")
async def fixture_engine():
    """Create test database engine."""
    # Store original DATABASE_URL if it exists
    original_database_url = os.environ.get("DATABASE_URL")
    
    # Set the test database URL
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    get_settings.cache_clear() # Clear lru_cache for settings
    
    # Re-get settings *after* environment variable is set and cache cleared
    settings_for_test = get_settings()

    # Create the test engine
    test_engine = create_async_engine(
        settings_for_test.database_url,
    )
    set_engine(test_engine) # Inject the test engine into src.models.database
    
    # Create all tables including users
    async with test_engine.begin() as conn: # This transaction is for DDL, not for test data
        await conn.run_sync(SQLModel.metadata.create_all)
    yield test_engine
    
    # Drop all tables after the session is complete
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await test_engine.dispose()

@pytest.fixture(name="client")
def fixture_client(engine: AsyncEngine): # Client now receives AsyncSession
    """Create test client with dependency overrides."""

    async def override_get_async_session(): # Must be async
        async with AsyncSession(engine) as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_async_session # Override get_async_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_id() -> UUID:
    """Return a sample user ID for testing."""
    return uuid4()


@pytest.fixture
async def test_user(session: AsyncSession) -> User: # Make fixture async
    """Create a test user with hashed password and a unique username."""
    unique_id = uuid4()
    user = User(
        username=f"testuser_{unique_id.hex}", # Ensure unique username
        email=f"test_{unique_id}@example.com",
        password_hash=auth_service.get_password_hash("testpassword123"),
    )
    session.add(user)
    await session.commit()  # Commit the user
    await session.refresh(user) # Refresh to get ID from DB
    return user


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    """Create authorization headers with valid JWT token."""
    settings = get_settings()
    token = auth_service.create_access_token(
        data={"sub": str(test_user.id), "email": test_user.email, "type": "access"},
        expires_delta=timedelta(minutes=settings.jwt_expiration_minutes)
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def different_user(session: AsyncSession) -> User: # Make fixture async
    """Create a different test user with a unique username."""
    unique_id = uuid4()
    user = User(
        username=f"otheruser_{unique_id.hex}", # Ensure unique username
        email=f"other_{unique_id}@example.com",
        password_hash=auth_service.get_password_hash("otherpassword456"),
    )
    session.add(user)
    await session.commit()  # Commit the user
    await session.refresh(user) # Refresh to get ID from DB
    return user


@pytest.fixture
def different_user_headers(different_user: User) -> dict:
    """Create authorization headers for different user."""
    settings = get_settings()
    token = auth_service.create_access_token(
        data={"sub": str(different_user.id), "email": different_user.email, "type": "access"},
        expires_delta=timedelta(minutes=settings.jwt_expiration_minutes)
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def expired_token(test_user: User) -> str:
    """Create an expired JWT token for testing."""
    token = auth_service.create_access_token(
        data={"sub": str(test_user.id), "email": test_user.email, "type": "access"},
        expires_delta=timedelta(minutes=-1)  # Already expired
    )
    return token


@pytest.fixture
def expired_auth_headers(expired_token: str) -> dict:
    """Create authorization headers with expired JWT token."""
    return {"Authorization": f"Bearer {expired_token}"}


@pytest.fixture
async def sample_task(session: AsyncSession, test_user: User) -> Task:
    """Create and return a sample task that is committed to the DB."""
    task = Task(
        user_id=test_user.id,
        title="Sample Task Title",
        description="Sample Task Description",
        is_complete=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Attach the user_id for test access, which is just test_user.id
    task._test_user_id = test_user.id
    return task
