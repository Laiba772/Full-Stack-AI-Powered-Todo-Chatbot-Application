"""Integration tests for user authentication (sign in)."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession


class TestSignIn:
    """Tests for POST /api/auth/signin."""

    @pytest.mark.asyncio
    async def test_health_check(self, client: TestClient):
        """Temporary test to check if the client can reach any endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @pytest.mark.asyncio
    async def test_signin_success(self, client: TestClient, test_user):
        """Test successful user authentication."""
        response = client.post(
            "/api/auth/signin",
            json={
                "email": test_user.email,
                "password": "testpassword123"
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0

    @pytest.mark.asyncio
    async def test_signin_wrong_password(self, client: TestClient, test_user):
        """Test that wrong password returns 401."""
        response = client.post(
            "/api/auth/signin",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            },
        )
        assert response.status_code == 401
        data = response.json()
        assert data["error"]["code"] == "INVALID_CREDENTIALS"
        # Generic message (not revealing which field is wrong)
        assert "Invalid email or password" in data["error"]["message"]

    @pytest.mark.asyncio
    async def test_signin_nonexistent_email(self, client: TestClient):
        """Test that nonexistent email returns 401."""
        response = client.post(
            "/api/auth/signin",
            json={
                "email": "nonexistent@example.com",
                "password": "somepassword123"
            },
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_signin_invalid_email_format(self, client: TestClient):
        """Test that invalid email format returns 422."""
        response = client.post(
            "/api/auth/signin",
            json={
                "email": "not-an-email",
                "password": "somepassword123"
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signin_missing_email(self, client: TestClient):
        """Test that missing email returns 422."""
        response = client.post(
            "/api/auth/signin",
            json={"password": "somepassword123"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signin_missing_password(self, client: TestClient):
        """Test that missing password returns 422."""
        response = client.post(
            "/api/auth/signin",
            json={"email": "test@example.com"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signin_returns_jwt_for_valid_user(self, client: TestClient, test_user):
        """Test that signin returns a valid JWT that can be decoded."""
        response = client.post(
            "/api/auth/signin",
            json={
                "email": "test@example.com",
                "password": "testpassword123"
            },
        )
        assert response.status_code == 200
        token = response.json()["token"]
        # Token should have 3 parts
        parts = token.split(".")
        assert len(parts) == 3
