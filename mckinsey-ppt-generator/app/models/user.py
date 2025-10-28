from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import BaseModel
from app.core.database import SQLALCHEMY_DATABASE_URL

# Use String for UUID fields if SQLite
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    UUID_FIELD = String(36)
else:
    from sqlalchemy.dialects.postgresql import UUID
    UUID_FIELD = UUID(as_uuid=True)

class UserRole(enum.Enum):
    """User roles for authorization"""
    ADMIN = "admin"
    USER = "user"
    PREMIUM = "premium"
    GUEST = "guest"

class UserStatus(enum.Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class User(BaseModel):
    """User model for authentication"""
    __tablename__ = "users"
    
    # Basic information
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    
    # Authentication
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Role and permissions
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE)
    
    # Usage limits
    daily_ppt_limit = Column(Integer, default=5)  # Daily PPT generation limit
    total_ppts_generated = Column(Integer, default=0)
    storage_limit_mb = Column(Integer, default=100)  # Storage limit in MB
    
    # Timestamps
    last_login = Column(DateTime(timezone=True))
    password_changed_at = Column(DateTime(timezone=True))
    
    # Profile
    company = Column(String(255))
    department = Column(String(255))
    phone = Column(String(50))
    
    # Settings
    preferences = Column(String)  # JSON string of user preferences
    language = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    
    # Relationships
    presentations = relationship("Presentation", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan", foreign_keys="[RefreshToken.user_id]")

class RefreshToken(BaseModel):
    """Refresh token storage for JWT authentication"""
    __tablename__ = "refresh_tokens"
    
    token = Column(String(500), unique=True, nullable=False, index=True)
    user_id = Column(UUID_FIELD, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    
    # Device information
    device_name = Column(String(255))
    ip_address = Column(String(45))  # Support IPv6
    user_agent = Column(String(500))
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")