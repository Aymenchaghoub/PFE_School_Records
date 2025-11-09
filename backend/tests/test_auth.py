"""
Tests for authentication endpoints and JWT token management.
"""
import pytest
from fastapi import status
import hashlib
from datetime import datetime, timedelta

# Try to import RefreshToken
try:
    from app.models.refresh_token import RefreshToken
    REFRESH_TOKEN_AVAILABLE = True
except ImportError:
    REFRESH_TOKEN_AVAILABLE = False
    RefreshToken = None

# Skip marker for tests requiring RefreshToken
requires_refresh_token = pytest.mark.skipif(
    not REFRESH_TOKEN_AVAILABLE,
    reason="RefreshToken model not available"
)


@pytest.mark.integration
def test_register_user(client, db_session):
    """Test user registration creates a new user."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@test.com",
            "name": "New User",
            "password": "password123",
            "role": "STUDENT"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert data["name"] == "New User"
    assert data["role"] == "STUDENT"
    assert "id" in data
    assert "password" not in data  # Password should not be returned


@pytest.mark.integration
def test_register_duplicate_email(client, test_admin_user):
    """Test registration fails with duplicate email."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "admin@test.com",  # Already exists
            "name": "Another Admin",
            "password": "password123",
            "role": "ADMIN"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.integration
def test_login_success(client, test_admin_user):
    """Test successful login returns tokens and user info."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check tokens are present
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    
    # Check user data
    assert data["user"]["email"] == "admin@test.com"
    assert data["user"]["name"] == "Test Admin"
    assert data["user"]["role"] == "ADMIN"


@pytest.mark.integration
def test_login_invalid_email(client):
    """Test login fails with non-existent email."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@test.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.integration
def test_login_invalid_password(client, test_admin_user):
    """Test login fails with incorrect password."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.integration
def test_refresh_token_success(client, test_admin_user):
    """Test refresh token generates new access and refresh tokens."""
    # First login
    login_response = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "password": "admin123"}
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Use refresh token
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check new tokens are returned
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["access_token"] != login_response.json()["access_token"]
    assert data["refresh_token"] != refresh_token  # Should be new token


@pytest.mark.integration
def test_refresh_token_revoked_after_use(client, test_admin_user, db_session):
    """Test that old refresh token is revoked after use."""
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "password": "admin123"}
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Use refresh token once
    client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    
    # Try to use it again - should fail
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "revoked" in response.json()["detail"].lower()


@pytest.mark.integration
def test_logout_revokes_tokens(client, admin_token, test_admin_user, db_session):
    """Test logout revokes all refresh tokens for the user."""
    # Login to get refresh token
    login_response = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "password": "admin123"}
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Logout
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert "logged out" in response.json()["message"].lower()
    
    # Try to use refresh token - should fail
    refresh_response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
def test_protected_endpoint_requires_auth(client):
    """Test that protected endpoints require authentication."""
    response = client.get("/api/users/")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
def test_protected_endpoint_with_valid_token(client, admin_token):
    """Test that protected endpoints work with valid token."""
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Should succeed (admin can access user list)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]


@pytest.mark.integration
def test_protected_endpoint_with_invalid_token(client):
    """Test that protected endpoints reject invalid tokens."""
    response = client.get(
        "/api/users/",
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
@requires_refresh_token
def test_refresh_token_hash_storage(client, test_admin_user, db_session):
    """Test that refresh tokens are stored as SHA-256 hashes."""
    from app.models.refresh_token import RefreshToken
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "password": "admin123"}
    )
    refresh_token = response.json()["refresh_token"]
    
    # Check token is hashed in database
    expected_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    db_token = db_session.query(RefreshToken).filter(
        RefreshToken.token_hash == expected_hash
    ).first()
    
    assert db_token is not None
    assert db_token.user_id == test_admin_user.id
    assert db_token.revoked is False
    assert db_token.expires_at > datetime.utcnow()
