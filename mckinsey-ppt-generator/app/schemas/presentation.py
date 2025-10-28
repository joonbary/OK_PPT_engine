from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class SlideLayout(str, Enum):
    """Available slide layouts"""
    TITLE = "title"
    CONTENT = "content"
    TWO_COLUMN = "two_column"
    CHART = "chart"
    TABLE = "table"
    IMAGE = "image"
    BLANK = "blank"
    SECTION_HEADER = "section_header"
    COMPARISON = "comparison"
    TIMELINE = "timeline"

class ChartType(str, Enum):
    """Available chart types"""
    COLUMN = "column"
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    AREA = "area"
    SCATTER = "scatter"

class SlideRequest(BaseModel):
    """Request schema for creating a slide"""
    title: str = Field(..., min_length=1, max_length=255)
    subtitle: Optional[str] = None
    content: Optional[List[str]] = None
    layout_type: SlideLayout = SlideLayout.CONTENT
    speaker_notes: Optional[str] = None
    
    # Chart data
    chart_type: Optional[ChartType] = None
    chart_data: Optional[Dict[str, List[float]]] = None
    
    # Table data
    table_headers: Optional[List[str]] = None
    table_data: Optional[List[List[str]]] = None
    
    # Image
    image_url: Optional[str] = None
    image_caption: Optional[str] = None
    
    # Two-column content
    left_content: Optional[List[str]] = None
    right_content: Optional[List[str]] = None

class PresentationRequest(BaseModel):
    """Request schema for creating a presentation"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    slides: List[SlideRequest] = Field(..., min_items=1)
    template_id: Optional[str] = None
    
    # Customization
    company_name: Optional[str] = None
    author_name: Optional[str] = None
    
    # Settings
    include_page_numbers: bool = True
    include_date: bool = True
    language: str = "en"
    
    @validator('slides')
    def validate_slides(cls, v):
        if len(v) > 100:
            raise ValueError("Maximum 100 slides allowed per presentation")
        return v

class PresentationResponse(BaseModel):
    """Response schema for presentation"""
    id: str
    title: str
    description: Optional[str] = None
    status: str
    slide_count: int
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user_email: str
    
    class Config:
        from_attributes = True

class PresentationListResponse(BaseModel):
    """Response schema for listing presentations"""
    presentations: List[PresentationResponse]
    total: int
    page: int
    page_size: int
    pages: int

class TemplateRequest(BaseModel):
    """Request schema for creating a template"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    
    # Style settings
    primary_color: Optional[str] = "#0070C0"
    secondary_color: Optional[str] = "#002E6C"
    font_family: Optional[str] = "Calibri"
    title_font_size: Optional[int] = 32
    body_font_size: Optional[int] = 16

class TemplateResponse(BaseModel):
    """Response schema for template"""
    id: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    usage_count: int
    rating: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class GenerateRequest(BaseModel):
    """Request schema for AI-powered presentation generation"""
    topic: str = Field(..., min_length=1, max_length=500)
    purpose: str = Field(..., description="Purpose of presentation: executive_summary, proposal, analysis, report")
    target_audience: str = Field(default="executives", description="Target audience")
    slide_count: int = Field(default=10, ge=3, le=30)
    
    # Content guidelines
    key_points: Optional[List[str]] = None
    tone: str = Field(default="professional", description="Tone: professional, formal, casual, technical")
    include_charts: bool = True
    include_images: bool = False
    
    # Customization
    company_name: Optional[str] = None
    template_id: Optional[str] = None
    language: str = "en"
    
    @validator('purpose')
    def validate_purpose(cls, v):
        valid_purposes = ['executive_summary', 'proposal', 'analysis', 'report', 'strategy', 'training']
        if v not in valid_purposes:
            raise ValueError(f"Purpose must be one of: {', '.join(valid_purposes)}")
        return v

class PresentationStats(BaseModel):
    """Presentation statistics"""
    total_presentations: int
    presentations_this_month: int
    total_slides: int
    average_slides_per_presentation: float
    most_used_template: Optional[str] = None
    storage_used_mb: float
    
class UserQuota(BaseModel):
    """User quota information"""
    daily_limit: int
    daily_used: int
    remaining_today: int
    storage_limit_mb: int
    storage_used_mb: float
    is_premium: bool