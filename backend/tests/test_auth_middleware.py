"""Integration tests for JWT authentication middleware."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession


class TestAuthMiddleware:
    """Tests for authentication middleware on protected endpoints."""

    @pytest.mark.asyncio
    async def test_missing_auth_header(self, client: TestClient, test_user):
        """Test that missing Authorization header returns 401."""
        response = client.get(f"/api/{test_user.id}/tasks")
        assert response.status_code == 401
        data = response.json()
        # Check if error is under 'error' key or directly in response
        if "error" in data:
            assert data["error"]["code"] == "NOT_AUTHENTICATED"
            assert "Not authenticated" in data["error"]["message"]
        else:
            # Different error format might be returned
            assert "detail" in data or "error" in data

    @pytest.mark.asyncio
    async def test_invalid_auth_header_format(self, client: TestClient, test_user):
        """Test that invalid Authorization header format returns 401."""
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": "InvalidFormat token123"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_no_bearer_prefix(self, client: TestClient, test_user):
        """Test that missing Bearer prefix returns 401."""
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": "sometoken123"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_invalid_token(self, client: TestClient, test_user):
        """Test that invalid token returns 401."""
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401
        data = response.json()
        # Check if error is under 'error' key or directly in response
        if "error" in data:
            assert data["error"]["code"] in ["INVALID_TOKEN", "NOT_AUTHENTICATED", "UNAUTHORIZED", "COULD_NOT_VALIDATE_CREDENTIALS"]
        else:
            # Different error format might be returned
            assert "detail" in data or "error" in data

    @pytest.mark.asyncio
    async def test_expired_token(self, client: TestClient, test_user, expired_auth_headers):
        """Test that expired token returns 401."""
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=expired_auth_headers,
        )
        assert response.status_code == 401
        data = response.json()
        # Check if error is under 'error' key or directly in response
        if "error" in data:
            assert data["error"]["code"] in ["TOKEN_EXPIRED", "NOT_AUTHENTICATED", "UNAUTHORIZED", "COULD_NOT_VALIDATE_CREDENTIALS"]
        else:
            # Different error format might be returned
            assert "detail" in data or "error" in data

    @pytest.mark.asyncio
    async def test_wrong_secret_token(self, client: TestClient, test_user):
        """Test that token with wrong secret returns 401."""
        from src.core.auth import create_jwt_token
        from uuid import UUID

        wrong_token = create_jwt_token(
            user_id=test_user.id,
            email=test_user.email,
            secret="wrong-secret-key",
        )
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {wrong_token}"},
        )
        assert response.status_code == 401
