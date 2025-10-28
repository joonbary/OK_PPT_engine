from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole, UserStatus

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    language: str = "en"
    timezone: str = "UTC"

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)
    password_confirm: str
    
    @validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

class UserUpdate(BaseModel):
    """Schema for user profile update"""
    full_name: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None

class UserInDB(UserBase):
    """User schema with database fields"""
    id: str
    role: UserRole
    status: UserStatus
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    daily_ppt_limit: int
    total_ppts_generated: int
    storage_limit_mb: int
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    """User response schema"""
    id: str
    email: str
    username: str
    full_name: Optional[str] = None
    role: str
    status: str
    is_verified: bool
    is_active: bool
    created_at: datetime
    company: Optional[str] = None
    department: Optional[str] = None
    daily_ppt_limit: int
    total_ppts_generated: int
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    """Login request schema"""
    username_or_email: str
    password: str
    remember_me: bool = False

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # seconds

class TokenData(BaseModel):
    """Token payload data"""
    sub: str  # user_id
    email: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[datetime] = None

class PasswordChange(BaseModel):
    """Password change schema"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    new_password_confirm: str
    
    @validator('new_password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

class PasswordReset(BaseModel):
    """Password reset schema"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)
    new_password_confirm: str
    
    @validator('new_password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v