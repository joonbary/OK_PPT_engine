"""Pydantic 스키마 정의"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PPTRequest(BaseModel):
    document: str = Field(..., min_length=100, description="비즈니스 문서 내용")
    style: str = Field(default="mckinsey", description="PPT 스타일")
    target_audience: str = Field(default="executive", description="타겟 청중")
    num_slides: int = Field(default=12, ge=5, le=30, description="슬라이드 수")
    language: str = Field(default="ko", description="언어")

class PPTResponse(BaseModel):
    ppt_id: str
    status: str
    estimated_time: int
    created_at: datetime
    
class StatusResponse(BaseModel):
    ppt_id: str
    status: str
    progress: int
    current_stage: Optional[str]
    quality_score: Optional[float]
    download_url: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
