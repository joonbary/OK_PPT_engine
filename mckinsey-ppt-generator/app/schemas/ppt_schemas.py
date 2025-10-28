"""
PPT 생성 관련 Pydantic 스키마
요청/응답 모델 정의
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

class JobStatus(str, Enum):
    """작업 상태"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PPTRequest(BaseModel):
    """PPT 생성 요청 스키마"""
    
    document: str = Field(..., min_length=10, description="입력 문서 텍스트")
    num_slides: int = Field(default=10, ge=1, le=100, description="생성할 슬라이드 수")
    target_audience: Optional[str] = Field(default="executive", description="대상 청중")
    presentation_purpose: Optional[str] = Field(default="analysis", description="프레젠테이션 목적")
    template: Optional[str] = Field(default="McKinsey Professional", description="사용할 템플릿")
    enable_ai_enhancement: bool = Field(default=True, description="AI 개선 사용 여부")
    
    @validator('document')
    def validate_document(cls, v):
        """문서 유효성 검증"""
        if len(v.strip()) < 10:
            raise ValueError("문서는 최소 10자 이상이어야 합니다")
        return v.strip()
    
    @validator('target_audience')
    def validate_audience(cls, v):
        """대상 청중 유효성 검증"""
        valid_audiences = ["executive", "technical", "general", "investor", "academic"]
        if v and v.lower() not in valid_audiences:
            raise ValueError(f"대상 청중은 {valid_audiences} 중 하나여야 합니다")
        return v.lower() if v else "executive"
    
    @validator('presentation_purpose')
    def validate_purpose(cls, v):
        """프레젠테이션 목적 유효성 검증"""
        valid_purposes = ["analysis", "proposal", "report", "training", "pitch"]
        if v and v.lower() not in valid_purposes:
            raise ValueError(f"프레젠테이션 목적은 {valid_purposes} 중 하나여야 합니다")
        return v.lower() if v else "analysis"
    
    class Config:
        json_schema_extra = {
            "example": {
                "document": "우리 회사의 2024년 매출은 1000억원으로 전년 대비 20% 증가했습니다...",
                "num_slides": 10,
                "target_audience": "executive",
                "presentation_purpose": "analysis",
                "template": "McKinsey Professional",
                "enable_ai_enhancement": True
            }
        }

class QualityBreakdown(BaseModel):
    """품질 점수 세부 내역"""
    
    clarity: float = Field(..., ge=0, le=1, description="명확성 점수")
    insight: float = Field(..., ge=0, le=1, description="인사이트 점수")
    structure: float = Field(..., ge=0, le=1, description="구조 점수")
    visual: float = Field(..., ge=0, le=1, description="시각적 품질 점수")
    actionability: float = Field(..., ge=0, le=1, description="실행가능성 점수")

class PPTResponse(BaseModel):
    """PPT 생성 응답 스키마"""
    
    job_id: UUID = Field(..., description="작업 ID")
    status: JobStatus = Field(..., description="작업 상태")
    download_url: Optional[str] = Field(None, description="다운로드 URL")
    file_path: Optional[str] = Field(None, description="파일 경로")
    quality_score: Optional[float] = Field(None, ge=0, le=1, description="품질 점수")
    quality_breakdown: Optional[QualityBreakdown] = Field(None, description="품질 점수 세부 내역")
    slides_generated: Optional[int] = Field(None, description="생성된 슬라이드 수")
    processing_time: Optional[float] = Field(None, description="처리 시간 (초)")
    error_message: Optional[str] = Field(None, description="에러 메시지")
    created_at: datetime = Field(..., description="생성 시간")
    completed_at: Optional[datetime] = Field(None, description="완료 시간")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "completed",
                "download_url": "/api/v1/presentations/download/123e4567-e89b-12d3-a456-426614174000",
                "file_path": "output/presentations/presentation_20250110_123456.pptx",
                "quality_score": 0.87,
                "quality_breakdown": {
                    "clarity": 0.85,
                    "insight": 0.88,
                    "structure": 0.90,
                    "visual": 0.82,
                    "actionability": 0.86
                },
                "slides_generated": 10,
                "processing_time": 45.2,
                "created_at": "2025-01-10T12:34:56",
                "completed_at": "2025-01-10T12:35:41"
            }
        }

class StatusResponse(BaseModel):
    """작업 상태 조회 응답"""
    
    job_id: UUID = Field(..., description="작업 ID")
    status: JobStatus = Field(..., description="현재 상태")
    progress: Optional[int] = Field(None, ge=0, le=100, description="진행률 (%)")
    current_step: Optional[str] = Field(None, description="현재 진행 중인 단계")
    estimated_time_remaining: Optional[int] = Field(None, description="예상 남은 시간 (초)")
    message: Optional[str] = Field(None, description="상태 메시지")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "in_progress",
                "progress": 65,
                "current_step": "Generating slides",
                "estimated_time_remaining": 15,
                "message": "슬라이드 7/10 생성 중..."
            }
        }

class AgentLogEntry(BaseModel):
    """에이전트 로그 엔트리"""
    
    agent_type: str = Field(..., description="에이전트 타입")
    agent_name: str = Field(..., description="에이전트 이름")
    execution_time: float = Field(..., description="실행 시간 (초)")
    success: bool = Field(..., description="성공 여부")
    tokens_used: Optional[int] = Field(None, description="사용된 토큰 수")
    error_message: Optional[str] = Field(None, description="에러 메시지")

class JobDetails(BaseModel):
    """작업 상세 정보"""
    
    job_id: UUID
    status: JobStatus
    input_document: str
    num_slides: int
    target_audience: str
    presentation_purpose: str
    quality_score: Optional[float]
    quality_breakdown: Optional[QualityBreakdown]
    agent_logs: List[AgentLogEntry]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    processing_time_seconds: Optional[float]
    error_message: Optional[str]

class BatchPPTRequest(BaseModel):
    """배치 PPT 생성 요청"""
    
    documents: List[PPTRequest] = Field(..., min_length=1, max_length=10, description="PPT 요청 목록")
    priority: Optional[int] = Field(default=0, ge=0, le=10, description="우선순위")
    
    class Config:
        json_schema_extra = {
            "example": {
                "documents": [
                    {
                        "document": "첫 번째 문서 내용...",
                        "num_slides": 10,
                        "target_audience": "executive"
                    },
                    {
                        "document": "두 번째 문서 내용...",
                        "num_slides": 8,
                        "target_audience": "technical"
                    }
                ],
                "priority": 5
            }
        }

class BatchPPTResponse(BaseModel):
    """배치 PPT 생성 응답"""
    
    batch_id: UUID = Field(..., description="배치 ID")
    job_ids: List[UUID] = Field(..., description="개별 작업 ID 목록")
    status: str = Field(..., description="배치 상태")
    total_jobs: int = Field(..., description="전체 작업 수")
    completed_jobs: int = Field(default=0, description="완료된 작업 수")