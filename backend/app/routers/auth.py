from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import LoginRequest, TokenResponse, UserCreate, UserResponse, RefreshTokenRequest
from app.core.security import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token, verify_token,
    get_current_user
)
from datetime import datetime, timedelta
import hashlib

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access/refresh tokens with token rotation."""
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    # Store refresh token hash in database
    from app.models.refresh_token import RefreshToken
    from app.core.config import settings
    
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    expires_at = datetime.utcnow() + timedelta(days=settings.jwt_refresh_expire_days)
    
    db_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token with token rotation and revocation."""
    from app.models.refresh_token import RefreshToken
    from app.core.config import settings
    
    # Verify token signature and expiration
    payload = verify_token(request.refresh_token, token_type="refresh")
    user_id = payload.get("sub")
    
    # Hash the provided token
    token_hash = hashlib.sha256(request.refresh_token.encode()).hexdigest()
    
    # Check if token exists in database and is not revoked
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.user_id == user_id,
        RefreshToken.revoked == False
    ).first()
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked refresh token"
        )
    
    # Check if token is expired
    if db_token.expires_at < datetime.utcnow():
        db_token.revoked = True
        db_token.revoked_at = datetime.utcnow()
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Revoke old token
    db_token.revoked = True
    db_token.revoked_at = datetime.utcnow()
    
    # Create new tokens
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    new_refresh_token = create_refresh_token(data={"sub": user.id})
    
    # Store new refresh token
    new_token_hash = hashlib.sha256(new_refresh_token.encode()).hexdigest()
    expires_at = datetime.utcnow() + timedelta(days=settings.jwt_refresh_expire_days)
    
    new_db_token = RefreshToken(
        user_id=user.id,
        token_hash=new_token_hash,
        expires_at=expires_at
    )
    db.add(new_db_token)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout and revoke all refresh tokens for the user."""
    from app.models.refresh_token import RefreshToken
    
    # Revoke all active refresh tokens for this user
    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id,
        RefreshToken.revoked == False
    ).update({
        "revoked": True,
        "revoked_at": datetime.utcnow()
    })
    db.commit()
    
    return {
        "message": "Successfully logged out",
        "detail": "All refresh tokens have been revoked"
    }
