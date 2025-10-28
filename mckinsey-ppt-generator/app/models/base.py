from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.sql import func
import uuid
from app.core.database import Base, SQLALCHEMY_DATABASE_URL

# Check if using SQLite or PostgreSQL
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    from sqlalchemy import String as UUID_TYPE
    def generate_uuid():
        return str(uuid.uuid4())
else:
    from sqlalchemy.dialects.postgresql import UUID
    UUID_TYPE = UUID(as_uuid=True)
    def generate_uuid():
        return uuid.uuid4()

class BaseModel(Base):
    """Base model with common fields"""
    __abstract__ = True
    
    id = Column(
        String(36) if "sqlite" in SQLALCHEMY_DATABASE_URL else UUID_TYPE,
        primary_key=True,
        default=generate_uuid,
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )
    
    def dict(self):
        """Convert model to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }