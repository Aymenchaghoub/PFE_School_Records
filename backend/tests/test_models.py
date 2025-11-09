"""
Tests for SQLAlchemy models and their relationships.
"""
import pytest
from datetime import datetime, timedelta
from app.models.user import User, UserRole
from app.core.security import get_password_hash
import hashlib

# Try to import RefreshToken, skip tests if not available
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


@pytest.mark.unit
def test_user_model_creation(db_session):
    """Test User model can be created and stored."""
    user = User(
        email="testuser@example.com",
        name="Test User",
        password=get_password_hash("password123"),
        role=UserRole.STUDENT
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "testuser@example.com"
    assert user.name == "Test User"
    assert user.role == UserRole.STUDENT
    assert user.password != "password123"  # Should be hashed


@pytest.mark.unit
def test_user_email_unique_constraint(db_session):
    """Test that duplicate emails are not allowed."""
    user1 = User(
        email="duplicate@example.com",
        name="User One",
        password=get_password_hash("password123"),
        role=UserRole.STUDENT
    )
    db_session.add(user1)
    db_session.commit()
    
    # Try to create another user with same email
    user2 = User(
        email="duplicate@example.com",
        name="User Two",
        password=get_password_hash("password456"),
        role=UserRole.TEACHER
    )
    db_session.add(user2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db_session.commit()


@pytest.mark.unit
def test_user_roles_enum(db_session):
    """Test that all UserRole enum values work."""
    roles = [UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT, UserRole.PARENT]
    
    for i, role in enumerate(roles):
        user = User(
            email=f"user{i}@example.com",
            name=f"User {i}",
            password=get_password_hash("password123"),
            role=role
        )
        db_session.add(user)
    
    db_session.commit()
    
    # Verify all users were created
    users = db_session.query(User).all()
    assert len(users) == 4
    assert set(u.role for u in users) == set(roles)


@pytest.mark.unit
@requires_refresh_token
def test_refresh_token_model_creation(db_session, test_admin_user):
    """Test RefreshToken model can be created."""
    token_hash = hashlib.sha256(b"test_token").hexdigest()
    expires_at = datetime.utcnow() + timedelta(days=7)
    
    refresh_token = RefreshToken(
        user_id=test_admin_user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        revoked=False
    )
    
    db_session.add(refresh_token)
    db_session.commit()
    db_session.refresh(refresh_token)
    
    assert refresh_token.id is not None
    assert refresh_token.user_id == test_admin_user.id
    assert refresh_token.token_hash == token_hash
    assert refresh_token.revoked is False
    assert refresh_token.created_at is not None
    assert refresh_token.expires_at == expires_at


@pytest.mark.unit
@requires_refresh_token
def test_refresh_token_user_relationship(db_session, test_admin_user):
    """Test relationship between RefreshToken and User."""
    token_hash = hashlib.sha256(b"test_token").hexdigest()
    expires_at = datetime.utcnow() + timedelta(days=7)
    
    refresh_token = RefreshToken(
        user_id=test_admin_user.id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    
    db_session.add(refresh_token)
    db_session.commit()
    
    # Test accessing user from token
    assert refresh_token.user.id == test_admin_user.id
    assert refresh_token.user.email == test_admin_user.email
    
    # Test accessing tokens from user
    assert len(test_admin_user.refresh_tokens) == 1
    assert test_admin_user.refresh_tokens[0].token_hash == token_hash


@pytest.mark.unit
@requires_refresh_token
def test_refresh_token_cascade_delete(db_session, test_admin_user):
    """Test that deleting user cascades to refresh tokens."""
    # Create tokens
    for i in range(3):
        token_hash = hashlib.sha256(f"token_{i}".encode()).hexdigest()
        refresh_token = RefreshToken(
            user_id=test_admin_user.id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        db_session.add(refresh_token)
    
    db_session.commit()
    
    # Verify tokens exist
    tokens = db_session.query(RefreshToken).filter(
        RefreshToken.user_id == test_admin_user.id
    ).all()
    assert len(tokens) == 3
    
    # Delete user
    db_session.delete(test_admin_user)
    db_session.commit()
    
    # Verify tokens are also deleted (cascade)
    tokens_after = db_session.query(RefreshToken).all()
    assert len(tokens_after) == 0


@pytest.mark.unit
@requires_refresh_token
def test_refresh_token_unique_hash(db_session, test_admin_user):
    """Test that token_hash must be unique."""
    token_hash = hashlib.sha256(b"duplicate_token").hexdigest()
    expires_at = datetime.utcnow() + timedelta(days=7)
    
    token1 = RefreshToken(
        user_id=test_admin_user.id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db_session.add(token1)
    db_session.commit()
    
    # Try to create another token with same hash
    token2 = RefreshToken(
        user_id=test_admin_user.id,
        token_hash=token_hash,  # Same hash
        expires_at=expires_at
    )
    db_session.add(token2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db_session.commit()


@pytest.mark.unit
@requires_refresh_token
def test_refresh_token_revocation(db_session, test_admin_user):
    """Test token revocation workflow."""
    token_hash = hashlib.sha256(b"test_token").hexdigest()
    expires_at = datetime.utcnow() + timedelta(days=7)
    
    token = RefreshToken(
        user_id=test_admin_user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        revoked=False
    )
    
    db_session.add(token)
    db_session.commit()
    
    # Revoke token
    token.revoked = True
    token.revoked_at = datetime.utcnow()
    db_session.commit()
    
    # Verify revocation
    db_session.refresh(token)
    assert token.revoked is True
    assert token.revoked_at is not None
    assert token.revoked_at <= datetime.utcnow()


@pytest.mark.unit
def test_user_query_by_role(db_session):
    """Test querying users by role."""
    # Create users with different roles
    admin = User(email="admin@test.com", name="Admin", password="hash1", role=UserRole.ADMIN)
    teacher1 = User(email="teacher1@test.com", name="Teacher 1", password="hash2", role=UserRole.TEACHER)
    teacher2 = User(email="teacher2@test.com", name="Teacher 2", password="hash3", role=UserRole.TEACHER)
    student = User(email="student@test.com", name="Student", password="hash4", role=UserRole.STUDENT)
    
    db_session.add_all([admin, teacher1, teacher2, student])
    db_session.commit()
    
    # Query teachers
    teachers = db_session.query(User).filter(User.role == UserRole.TEACHER).all()
    assert len(teachers) == 2
    assert all(u.role == UserRole.TEACHER for u in teachers)
    
    # Query admin
    admins = db_session.query(User).filter(User.role == UserRole.ADMIN).all()
    assert len(admins) == 1
    assert admins[0].email == "admin@test.com"


@pytest.mark.unit
@requires_refresh_token
def test_refresh_token_expiration_check(db_session, test_admin_user):
    """Test checking if refresh token is expired."""
    # Create expired token
    expired_token = RefreshToken(
        user_id=test_admin_user.id,
        token_hash=hashlib.sha256(b"expired").hexdigest(),
        expires_at=datetime.utcnow() - timedelta(days=1),  # Expired yesterday
        revoked=False
    )
    
    # Create valid token
    valid_token = RefreshToken(
        user_id=test_admin_user.id,
        token_hash=hashlib.sha256(b"valid").hexdigest(),
        expires_at=datetime.utcnow() + timedelta(days=7),  # Expires in 7 days
        revoked=False
    )
    
    db_session.add_all([expired_token, valid_token])
    db_session.commit()
    
    # Check expiration
    assert expired_token.expires_at < datetime.utcnow()
    assert valid_token.expires_at > datetime.utcnow()
