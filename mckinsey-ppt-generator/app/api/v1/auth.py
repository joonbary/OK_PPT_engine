from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
from app.core.security import (
    verify_password, 
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    generate_verification_token,
    generate_password_reset_token
)
from app.core.logging import app_logger
from app.models.user import User, RefreshToken, UserRole, UserStatus
from app.schemas.auth import (
    UserCreate,
    UserResponse,
    LoginRequest,
    Token,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm
)
from app.api.deps import get_current_user, get_current_active_user

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        company=user_data.company,
        department=user_data.department,
        phone=user_data.phone,
        language=user_data.language,
        timezone=user_data.timezone,
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        is_verified=False,  # Email verification required
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate verification token (would send email in production)
    verification_token = generate_verification_token(new_user.email)
    app_logger.info(f"New user registered: {new_user.username} (ID: {new_user.id})")
    app_logger.debug(f"Verification token for {new_user.email}: {verification_token}")
    
    return UserResponse.from_orm(new_user)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login with username/email and password"""
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        app_logger.warning(f"Failed login attempt for: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    
    # Create tokens
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
        additional_claims={
            "email": user.email,
            "username": user.username,
            "role": user.role.value
        }
    )
    
    refresh_token = None
    if form_data.client_id == "remember_me":  # Use client_id field for remember_me
        refresh_token = create_refresh_token(subject=user.id)
        
        # Store refresh token in database
        refresh_token_obj = RefreshToken(
            token=refresh_token,
            user_id=user.id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )
        db.add(refresh_token_obj)
        db.commit()
    
    app_logger.info(f"User logged in: {user.username} (ID: {user.id})")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800  # 30 minutes in seconds
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    # Verify refresh token
    payload = verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if refresh token exists and is valid
    token_obj = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.is_revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()
    
    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found or expired"
        )
    
    # Get user
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=30)
    new_access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
        additional_claims={
            "email": user.email,
            "username": user.username,
            "role": user.role.value
        }
    )
    
    app_logger.info(f"Token refreshed for user: {user.username}")
    
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,  # Return same refresh token
        "token_type": "bearer",
        "expires_in": 1800
    }

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout and revoke refresh tokens"""
    # Revoke all user's refresh tokens
    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id,
        RefreshToken.is_revoked == False
    ).update({"is_revoked": True})
    db.commit()
    
    app_logger.info(f"User logged out: {current_user.username}")
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    return UserResponse.from_orm(current_user)

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    current_user.password_changed_at = datetime.now(timezone.utc)
    
    # Revoke all refresh tokens (force re-login)
    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id
    ).update({"is_revoked": True})
    
    db.commit()
    
    app_logger.info(f"Password changed for user: {current_user.username}")
    
    return {"message": "Password changed successfully"}

@router.post("/verify-email/{token}")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """Verify user email with token"""
    # In production, implement proper token verification
    # For now, just demonstrate the endpoint
    
    return {"message": "Email verification endpoint - implement with email service"}

@router.post("/password-reset")
async def request_password_reset(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """Request password reset email"""
    user = db.query(User).filter(User.email == reset_data.email).first()
    
    if user:
        # Generate reset token
        reset_token = generate_password_reset_token(user.email)
        app_logger.info(f"Password reset requested for: {user.email}")
        app_logger.debug(f"Reset token: {reset_token}")
        # In production, send email with reset link
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/password-reset/confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Confirm password reset with token"""
    # In production, implement proper token verification
    # For now, just demonstrate the endpoint
    
    return {"message": "Password reset confirmation endpoint - implement with email service"}