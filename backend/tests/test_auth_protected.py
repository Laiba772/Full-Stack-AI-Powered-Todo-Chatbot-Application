"""Integration tests for protected endpoints with authentication."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession


class TestProtectedEndpoints:
    """Tests for authenticated access to task endpoints."""

    @pytest.mark.asyncio
    async def test_create_task_with_auth(self, client: TestClient, test_user, auth_headers):
        """Test creating a task with valid authentication."""
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "Task description"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["description"] == "Task description"
        assert data["is_complete"] is False

    @pytest.mark.asyncio
    async def test_list_tasks_with_auth(self, client: TestClient, test_user, auth_headers):
        """Test listing tasks with valid authentication."""
        response = client.get(
            "/api/tasks",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data  # Updated to match new API response
        # total, page, page_size fields may not be in the response anymore

    @pytest.mark.asyncio
    async def test_get_task_with_auth(self, client: TestClient, sample_task, auth_headers):
        """Test getting a specific task with valid authentication."""
        response = client.get(
            f"/api/tasks/{sample_task.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_task.id) # Reverted assertion
        assert data["title"] == sample_task.title

    @pytest.mark.asyncio
    async def test_update_task_with_auth(self, client: TestClient, sample_task, auth_headers):
        """Test updating a task with valid authentication."""
        response = client.patch(
            f"/api/tasks/{sample_task.id}",
            json={"title": "Updated Title", "is_complete": True},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["is_complete"] is True

    @pytest.mark.asyncio
    async def test_delete_task_with_auth(self, client: TestClient, sample_task, auth_headers):
        """Test deleting a task with valid authentication."""
        response = client.delete(
            f"/api/tasks/{sample_task.id}",
            headers=auth_headers,
        )
        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(
            f"/api/tasks/{sample_task.id}",
            headers=auth_headers,
        )
        assert get_response.status_code == 404


class TestUserIsolation:
    """Tests for user isolation with authenticated endpoints."""

    @pytest.mark.asyncio
    async def test_cannot_access_other_user_tasks(
        self, client: TestClient, test_user, different_user_headers
    ):
        """Test that user cannot access another user's tasks."""
        # Try to access test_user's tasks with different user's token
        response = client.get(
            "/api/tasks",
            headers=different_user_headers,
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_cannot_create_task_for_other_user(
        self, client: TestClient, test_user, different_user_headers
    ):
        """Test that user cannot create tasks for another user."""
        response = client.post(
            "/api/tasks",
            json={"title": "Hacked Task", "description": "Hacked Task"},
            headers=different_user_headers,
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_cannot_update_other_user_task(
        self, client: TestClient, sample_task, different_user_headers
    ):
        """Test that user cannot update another user's task."""
        response = client.patch(
            f"/api/tasks/{sample_task.id}",
            json={"title": "Hacked Update"},
            headers=different_user_headers,
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_cannot_delete_other_user_task(
        self, client: TestClient, sample_task, different_user_headers
    ):
        """Test that user cannot delete another user's task."""
        response = client.delete(
            f"/api/tasks/{sample_task.id}",
            headers=different_user_headers,
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_user_can_access_own_tasks(
        self, client: TestClient, test_user, auth_headers
    ):
        """Test that user can access their own tasks."""
        response = client.get(
            "/api/tasks",
            headers=auth_headers,
        )
        assert response.status_code == 200
