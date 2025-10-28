from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.logging import app_logger
import secrets
import hashlib

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.SECRET_KEY or secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[dict] = None
) -> str:
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }
    
    if additional_claims:
        to_encode.update(additional_claims)
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    app_logger.debug(f"Access token created for subject: {subject}")
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT refresh token"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
        "jti": secrets.token_urlsafe(32)  # JWT ID for tracking
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    app_logger.debug(f"Refresh token created for subject: {subject}")
    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type
        if payload.get("type") != token_type:
            app_logger.warning(f"Invalid token type: expected {token_type}, got {payload.get('type')}")
            return None
        
        # Check expiration
        if payload.get("exp"):
            if datetime.fromtimestamp(payload["exp"], tz=timezone.utc) < datetime.now(timezone.utc):
                app_logger.warning("Token has expired")
                return None
        
        return payload
    except JWTError as e:
        app_logger.error(f"JWT verification failed: {str(e)}")
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def generate_password_reset_token(email: str) -> str:
    """Generate a password reset token"""
    data = f"{email}:{datetime.now(timezone.utc).isoformat()}:{secrets.token_urlsafe(16)}"
    token = hashlib.sha256(data.encode()).hexdigest()
    app_logger.info(f"Password reset token generated for: {email}")
    return token

def verify_password_reset_token(token: str, email: str, max_age_hours: int = 24) -> bool:
    """Verify a password reset token (simplified version)"""
    # In production, store tokens in database with expiration
    # This is a simplified implementation
    try:
        # Here you would check the token against database
        # For now, just return True for demonstration
        app_logger.info(f"Verifying password reset token for: {email}")
        return True
    except Exception as e:
        app_logger.error(f"Password reset token verification failed: {str(e)}")
        return False

def generate_verification_token(email: str) -> str:
    """Generate an email verification token"""
    data = f"{email}:{secrets.token_urlsafe(32)}"
    token = hashlib.sha256(data.encode()).hexdigest()
    app_logger.info(f"Verification token generated for: {email}")
    return token

def create_api_key() -> str:
    """Generate a new API key"""
    return f"mck_{secrets.token_urlsafe(32)}"