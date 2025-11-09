"""
Test configuration and fixtures for PFC backend tests.
Uses SQLite in-memory database for fast, isolated testing.
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole

# Try to import RefreshToken, but don't fail if it doesn't exist
try:
    from app.models.refresh_token import RefreshToken
    REFRESH_TOKEN_AVAILABLE = True
except ImportError:
    REFRESH_TOKEN_AVAILABLE = False


# Test database URL (SQLite in-memory)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine with special configuration for SQLite
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_admin_user(db_session):
    """Create a test admin user."""
    user = User(
        email="admin@test.com",
        name="Test Admin",
        password=get_password_hash("admin123"),
        role=UserRole.ADMIN
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_teacher_user(db_session):
    """Create a test teacher user."""
    user = User(
        email="teacher@test.com",
        name="Test Teacher",
        password=get_password_hash("teacher123"),
        role=UserRole.TEACHER
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_student_user(db_session):
    """Create a test student user."""
    user = User(
        email="student@test.com",
        name="Test Student",
        password=get_password_hash("student123"),
        role=UserRole.STUDENT
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_token(client, test_admin_user):
    """Get authentication token for admin user."""
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "password": "admin123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def teacher_token(client, test_teacher_user):
    """Get authentication token for teacher user."""
    response = client.post(
        "/api/auth/login",
        json={"email": "teacher@test.com", "password": "teacher123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def student_token(client, test_student_user):
    """Get authentication token for student user."""
    response = client.post(
        "/api/auth/login",
        json={"email": "student@test.com", "password": "student123"}
    )
    return response.json()["access_token"]
