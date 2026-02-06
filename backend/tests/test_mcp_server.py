from uuid import UUID, uuid4
from datetime import datetime
import pytest
from fastapi.testclient import TestClient # Use TestClient for synchronous tests
from sqlmodel import Session, SQLModel
import os

from src.main import app
from src.models.user import User
from src.models.task import Task
from src.core.auth import create_jwt_token
from src.config import settings
from src.schemas.task import AddTaskInput, TaskOutput, ListTasksOutput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput, StatusOutput
from src.models.database import get_async_session # Import get_async_session

# We will use the client and session fixtures from conftest.py
# Therefore, we remove the local database setup from this file.


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    """Create a test user with hashed password and a unique username/email."""
    user_uuid = uuid4()
    user = User(
        username=f"test_mcp_server_user_{user_uuid.hex}", # Ensure unique username
        email=f"test_mcp_server_user_{user_uuid}@example.com",
        password_hash="hashed_password"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_token")
def auth_token_fixture(test_user: User) -> str:
    """Create a JWT token for the test user."""
    return create_jwt_token(test_user.id, test_user.email, secret=settings.jwt_secret, expiration_minutes=settings.jwt_expiration_minutes)


def test_add_task_mcp_tool(client: TestClient, auth_token: str):
    task_description = "Test task from MCP"
    response = client.post(
        "/mcp/add_task",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"description": task_description}
    )

    assert response.status_code == 200
    task_output = TaskOutput(**response.json())
    assert task_output.description == task_description
    assert task_output.is_complete is False
    assert task_output.task_id is not None


def test_list_tasks_mcp_tool(client: TestClient, auth_token: str, test_user: User):
    # Add a task first
    client.post(
        "/mcp/add_task",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"description": "Task for listing"}
    )

    response = client.get(
        "/mcp/list_tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    list_output = ListTasksOutput(**response.json())
    assert len(list_output.tasks) == 1
    assert list_output.tasks[0].description == "Task for listing"


def test_update_task_mcp_tool(client: TestClient, auth_token: str, test_user: User):
    # Add a task first
    add_response = client.post(
        "/mcp/add_task",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"description": "Task to update"}
    )
    task_id = add_response.json()["task_id"]

    updated_description = "Updated task description"
    response = client.post(
        "/mcp/update_task",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"task_id": str(task_id), "description": updated_description, "is_complete": True}
    )

    assert response.status_code == 200
    task_output = TaskOutput(**response.json())
    assert task_output.task_id == UUID(task_id)
    assert task_output.description == updated_description
    assert task_output.is_complete is True


def test_complete_task_mcp_tool(client: TestClient, auth_token: str, test_user: User):
    # Add a task first
    add_response = client.post(
        "/mcp/add_task",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"description": "Task to complete"}
    )
    task_id = add_response.json()["task_id"]

    response = client.post(
        "/mcp/complete_task",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"task_id": str(task_id)}
    )

    assert response.status_code == 200
    status_output = StatusOutput(**response.json())
    assert status_output.task_id == UUID(task_id)
    assert status_output.status == "completed"

    # Verify task is complete in DB
    list_response = client.get(
        "/mcp/list_tasks?is_complete=true",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert list_response.status_code == 200
    list_output = ListTasksOutput(**list_response.json())
    assert len(list_output.tasks) == 1
    assert list_output.tasks[0].task_id == UUID(task_id)
    assert list_output.tasks[0].is_complete is True


def test_delete_task_mcp_tool(client: TestClient, auth_token: str, test_user: User):
    # Add a task first
    add_response = client.post(
        "/mcp/add_task",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"description": "Task to delete"}
    )
    task_id = add_response.json()["task_id"]

    response = client.post(
        "/mcp/delete_task",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"task_id": str(task_id)}
    )

    assert response.status_code == 200
    status_output = StatusOutput(**response.json())
    assert status_output.task_id == UUID(task_id)
    assert status_output.status == "deleted"

    # Verify task is deleted from DB
    list_response = client.get(
        "/mcp/list_tasks",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert list_response.status_code == 200
    list_output = ListTasksOutput(**list_response.json())
    assert len(list_output.tasks) == 0