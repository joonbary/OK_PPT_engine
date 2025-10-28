from sqlalchemy import Column, String, Text, JSON, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel
from app.core.database import SQLALCHEMY_DATABASE_URL

# Use String for UUID fields if SQLite
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    UUID_FIELD = String(36)
else:
    from sqlalchemy.dialects.postgresql import UUID
    UUID_FIELD = UUID(as_uuid=True)

class PresentationStatus(enum.Enum):
    """Presentation generation status"""
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"

class PresentationType(enum.Enum):
    """Types of presentations"""
    EXECUTIVE_SUMMARY = "executive_summary"
    STRATEGY_PROPOSAL = "strategy_proposal"
    MARKET_ANALYSIS = "market_analysis"
    FINANCIAL_REPORT = "financial_report"
    PROJECT_ROADMAP = "project_roadmap"
    CUSTOM = "custom"

class Presentation(BaseModel):
    """Presentation model"""
    __tablename__ = "presentations"
    
    title = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(SQLEnum(PresentationType), default=PresentationType.CUSTOM)
    status = Column(SQLEnum(PresentationStatus), default=PresentationStatus.DRAFT)
    
    # User information
    user_id = Column(UUID_FIELD, ForeignKey("users.id"), nullable=True)
    user_email = Column(String(255))
    
    # Presentation metadata (renamed from 'metadata' as it's reserved in SQLAlchemy)
    presentation_metadata = Column(JSON, default={})
    settings = Column(JSON, default={})
    
    # Content
    outline = Column(JSON)  # Presentation structure and outline
    content = Column(JSON)  # Actual slide content
    
    # File paths
    file_path = Column(String(500))  # Path to generated PPTX file
    thumbnail_path = Column(String(500))  # Path to thumbnail image
    
    # Statistics
    slide_count = Column(Integer, default=0)
    word_count = Column(Integer, default=0)
    
    # AI generation details
    ai_model = Column(String(100))
    ai_tokens_used = Column(Integer, default=0)
    generation_time = Column(Integer)  # Generation time in seconds
    
    # Relationships
    slides = relationship("Slide", back_populates="presentation", cascade="all, delete-orphan")
    user = relationship("User", back_populates="presentations")

class Slide(BaseModel):
    """Individual slide model"""
    __tablename__ = "slides"
    
    presentation_id = Column(UUID_FIELD, ForeignKey("presentations.id"), nullable=False)
    slide_number = Column(Integer, nullable=False)
    
    # Slide content
    title = Column(String(255))
    subtitle = Column(String(500))
    content = Column(JSON)  # Structured content (text, bullet points, etc.)
    
    # Layout and design
    layout_type = Column(String(100))  # title, content, two_column, etc.
    design_template = Column(String(100))
    
    # Media
    images = Column(JSON, default=[])  # List of image URLs or paths
    charts = Column(JSON, default=[])  # Chart data and configuration
    
    # Notes
    speaker_notes = Column(Text)
    
    # Relationships
    presentation = relationship("Presentation", back_populates="slides")

class Template(BaseModel):
    """PPT Template model"""
    __tablename__ = "templates"
    
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    category = Column(String(100))
    
    # Template configuration
    config = Column(JSON, nullable=False)  # Color scheme, fonts, layouts, etc.
    slides_config = Column(JSON)  # Default slide configurations
    
    # Usage statistics
    usage_count = Column(Integer, default=0)
    rating = Column(Integer, default=0)
    
    # File paths
    preview_path = Column(String(500))
    template_file = Column(String(500))