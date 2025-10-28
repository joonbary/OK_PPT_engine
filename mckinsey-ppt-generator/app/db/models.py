"""
데이터베이스 모델 정의
PPT 생성 작업, 에이전트 로그, 품질 메트릭 모델
"""

from sqlalchemy import Column, String, Float, DateTime, Integer, Text, JSON, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.db.session import Base

class JobStatus(enum.Enum):
    """작업 상태"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentType(enum.Enum):
    """에이전트 타입"""
    STRATEGIST = "strategist"
    ANALYST = "analyst"
    STORYTELLER = "storyteller"
    DESIGNER = "designer"
    REVIEWER = "reviewer"

class PPTGenerationJob(Base):
    """PPT 생성 작업 모델"""
    
    __tablename__ = "ppt_generation_jobs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Job information
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    input_document = Column(Text, nullable=False)
    num_slides = Column(Integer, default=10)
    target_audience = Column(String(100))
    presentation_purpose = Column(String(100))
    
    # Output information
    ppt_file_path = Column(String(500))
    quality_score = Column(Float)
    slides_generated = Column(Integer)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    processing_time_seconds = Column(Float)
    
    # User information
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user_email = Column(String(255))
    
    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Metadata
    job_metadata = Column(JSON)
    
    # Relationships
    agent_logs = relationship("AgentLog", back_populates="job", cascade="all, delete-orphan")
    quality_metrics = relationship("QualityMetrics", back_populates="job", uselist=False, cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "status": self.status.value if self.status else None,
            "input_document": self.input_document,
            "num_slides": self.num_slides,
            "target_audience": self.target_audience,
            "presentation_purpose": self.presentation_purpose,
            "ppt_file_path": self.ppt_file_path,
            "quality_score": self.quality_score,
            "slides_generated": self.slides_generated,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "processing_time_seconds": self.processing_time_seconds,
            "error_message": self.error_message
        }

class AgentLog(Base):
    """에이전트 실행 로그"""
    
    __tablename__ = "agent_logs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key
    job_id = Column(UUID(as_uuid=True), ForeignKey("ppt_generation_jobs.id"), nullable=False)
    
    # Agent information
    agent_type = Column(Enum(AgentType), nullable=False)
    agent_name = Column(String(100))
    
    # Execution details
    input_data = Column(JSON)
    output_data = Column(JSON)
    prompt = Column(Text)
    response = Column(Text)
    
    # Performance metrics
    execution_time_seconds = Column(Float)
    tokens_used = Column(Integer)
    model_used = Column(String(100))
    
    # Status
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    job = relationship("PPTGenerationJob", back_populates="agent_logs")

class QualityMetrics(Base):
    """품질 메트릭"""
    
    __tablename__ = "quality_metrics"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key
    job_id = Column(UUID(as_uuid=True), ForeignKey("ppt_generation_jobs.id"), nullable=False, unique=True)
    
    # Quality scores (0.0 - 1.0)
    clarity = Column(Float, nullable=False)
    insight = Column(Float, nullable=False)
    structure = Column(Float, nullable=False)
    visual = Column(Float, nullable=False)
    actionability = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    
    # Pass/Fail
    passed = Column(Boolean, default=False)
    target_score = Column(Float, default=0.85)
    
    # Detailed metrics
    so_what_pass_rate = Column(Float)
    avg_headline_quality = Column(Float)
    avg_insight_level = Column(Float)
    data_based_rate = Column(Float)
    comparison_rate = Column(Float)
    strategic_rate = Column(Float)
    actionable_rate = Column(Float)
    quantified_rate = Column(Float)
    prioritized_rate = Column(Float)
    
    # Metadata
    details = Column(JSON)
    improvement_suggestions = Column(JSON)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    job = relationship("PPTGenerationJob", back_populates="quality_metrics")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "clarity": self.clarity,
            "insight": self.insight,
            "structure": self.structure,
            "visual": self.visual,
            "actionability": self.actionability,
            "total": self.total,
            "passed": self.passed,
            "target_score": self.target_score,
            "so_what_pass_rate": self.so_what_pass_rate,
            "avg_headline_quality": self.avg_headline_quality,
            "avg_insight_level": self.avg_insight_level,
            "data_based_rate": self.data_based_rate,
            "comparison_rate": self.comparison_rate,
            "strategic_rate": self.strategic_rate,
            "actionable_rate": self.actionable_rate,
            "quantified_rate": self.quantified_rate,
            "prioritized_rate": self.prioritized_rate,
            "details": self.details,
            "improvement_suggestions": self.improvement_suggestions
        }