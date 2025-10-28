from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Optional, List
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path

from app.core.database import get_db
from app.core.logging import app_logger
from app.api.deps import get_current_user, get_current_verified_user
from app.models import User, Presentation, PresentationStatus, PresentationType
from app.schemas.presentation import (
    PresentationRequest,
    PresentationResponse,
    PresentationListResponse,
    GenerateRequest,
    PresentationStats,
    UserQuota
)
from app.services import PPTGenerator, SlideContent, PresentationMetadata

router = APIRouter(
    prefix="/api/v1/presentations",
    tags=["presentations"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create", response_model=PresentationResponse, status_code=status.HTTP_201_CREATED)
async def create_presentation(
    presentation_data: PresentationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Create a new presentation"""
    # Check user quota
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_presentations = db.query(func.count(Presentation.id)).filter(
        Presentation.user_id == current_user.id,
        Presentation.created_at >= today_start
    ).scalar()
    
    if today_presentations >= current_user.daily_ppt_limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Daily limit of {current_user.daily_ppt_limit} presentations reached"
        )
    
    # Create metadata
    metadata = PresentationMetadata(
        title=presentation_data.title,
        author=presentation_data.author_name or current_user.full_name or current_user.username,
        subject=presentation_data.description or "",
        category=presentation_data.presentation_type if hasattr(presentation_data, 'presentation_type') else "Business"
    )
    
    # Convert request slides to SlideContent objects
    slides = []
    for slide_req in presentation_data.slides:
        # Build charts list if chart data is provided
        charts = []
        if hasattr(slide_req, 'chart_type') and hasattr(slide_req, 'chart_data') and slide_req.chart_data:
            charts.append({
                "type": slide_req.chart_type,
                "title": slide_req.title,
                "categories": list(slide_req.chart_data.keys()),
                "series": [{
                    "name": "Values",
                    "values": list(slide_req.chart_data.values())
                }]
            })
        
        # Build tables list if table data is provided
        tables = []
        if hasattr(slide_req, 'table_headers') and hasattr(slide_req, 'table_data'):
            if slide_req.table_headers and slide_req.table_data:
                tables.append({
                    "headers": slide_req.table_headers,
                    "rows": slide_req.table_data
                })
        
        # Build images list if image is provided
        images = []
        if hasattr(slide_req, 'image_url') and slide_req.image_url:
            images.append(slide_req.image_url)
        
        slide_content = SlideContent(
            title=slide_req.title,
            subtitle=slide_req.subtitle if hasattr(slide_req, 'subtitle') else "",
            content=slide_req.content if hasattr(slide_req, 'content') else [],
            layout_type=slide_req.layout_type,
            speaker_notes=slide_req.speaker_notes if hasattr(slide_req, 'speaker_notes') else "",
            charts=charts,
            tables=tables,
            images=images
        )
        slides.append(slide_content)
    
    # Generate presentation
    try:
        generator = PPTGenerator(db)
        file_path, presentation_model = generator.create_presentation(
            slides_content=slides,
            metadata=metadata,
            template_name="McKinsey Professional",  # TODO: Get from template_id
            save_to_db=True
        )
        
        # Update user stats
        current_user.total_ppts_generated += 1
        db.commit()
        
        app_logger.info(f"Presentation created: {presentation_model.id} for user {current_user.username}")
        
        return PresentationResponse(
            id=str(presentation_model.id),
            title=presentation_model.title,
            description=presentation_model.description,
            status=presentation_model.status.value,
            slide_count=presentation_model.slide_count,
            file_path=presentation_model.file_path,
            download_url=f"/api/v1/presentations/{presentation_model.id}/download",
            created_at=presentation_model.created_at,
            updated_at=presentation_model.updated_at,
            user_email=presentation_model.user_email
        )
        
    except Exception as e:
        app_logger.error(f"Failed to create presentation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create presentation"
        )

@router.post("/generate", response_model=PresentationResponse)
async def generate_presentation(
    generate_data: GenerateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Generate a presentation using AI (placeholder for future LLM integration)"""
    # This is a placeholder for AI-powered generation
    # In production, this would call LLM APIs to generate content
    
    # For now, create a sample presentation
    sample_slides = [
        SlideContent(
            title=generate_data.topic,
            subtitle=f"Prepared for {generate_data.target_audience}",
            layout_type="title"
        ),
        SlideContent(
            title="Executive Summary",
            content=[
                "Key finding 1: Market opportunity identified",
                "Key finding 2: Strategic alignment confirmed",
                "Key finding 3: Implementation roadmap defined"
            ],
            layout_type="content"
        ),
        SlideContent(
            title="Market Analysis",
            content=["Current market size: $10B", "Growth rate: 15% CAGR"],
            charts=[{
                "type": "column",
                "title": "Market Growth Trend",
                "categories": ["2020", "2021", "2022", "2023", "2024"],
                "series": [{
                    "name": "Market Size ($B)",
                    "values": [100, 115, 132, 152, 175]
                }]
            }],
            layout_type="chart"
        ),
        SlideContent(
            title="Next Steps",
            content=[
                "Phase 1: Initial assessment (Q1 2024)",
                "Phase 2: Pilot implementation (Q2 2024)",
                "Phase 3: Full rollout (Q3-Q4 2024)"
            ],
            layout_type="content"
        )
    ]
    
    # Add more slides based on requested count
    for i in range(len(sample_slides), min(generate_data.slide_count, 10)):
        sample_slides.append(
            SlideContent(
                title=f"Analysis Point {i-2}",
                content=[f"Insight {j}" for j in range(1, 4)],
                layout_type="content"
            )
        )
    
    metadata = PresentationMetadata(
        title=generate_data.topic,
        author=current_user.full_name or current_user.username,
        subject=f"{generate_data.purpose.replace('_', ' ').title()} for {generate_data.target_audience}",
        category="Generated"
    )
    
    try:
        generator = PPTGenerator(db)
        file_path, presentation_model = generator.create_presentation(
            slides_content=sample_slides,
            metadata=metadata,
            template_name="McKinsey Professional",  # TODO: Get from template_id
            save_to_db=True
        )
        
        return PresentationResponse(
            id=str(presentation_model.id),
            title=presentation_model.title,
            description=presentation_model.description,
            status=presentation_model.status.value,
            slide_count=presentation_model.slide_count,
            file_path=presentation_model.file_path,
            download_url=f"/api/v1/presentations/{presentation_model.id}/download",
            created_at=presentation_model.created_at,
            updated_at=presentation_model.updated_at,
            user_email=presentation_model.user_email
        )
    except Exception as e:
        app_logger.error(f"Failed to generate presentation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate presentation"
        )

@router.get("/", response_model=PresentationListResponse)
async def list_presentations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's presentations"""
    query = db.query(Presentation).filter(
        Presentation.user_id == current_user.id,
        Presentation.is_deleted == False
    )
    
    if status:
        query = query.filter(Presentation.status == status)
    
    if search:
        query = query.filter(
            or_(
                Presentation.title.ilike(f"%{search}%"),
                Presentation.description.ilike(f"%{search}%")
            )
        )
    
    # Pagination
    total = query.count()
    offset = (page - 1) * page_size
    presentations = query.order_by(Presentation.created_at.desc()).offset(offset).limit(page_size).all()
    
    return PresentationListResponse(
        presentations=[PresentationResponse.from_orm(p) for p in presentations],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )

@router.get("/{presentation_id}", response_model=PresentationResponse)
async def get_presentation(
    presentation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific presentation"""
    presentation = db.query(Presentation).filter(
        Presentation.id == presentation_id,
        Presentation.user_id == current_user.id,
        Presentation.is_deleted == False
    ).first()
    
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation not found"
        )
    
    return PresentationResponse.from_orm(presentation)

@router.get("/{presentation_id}/download")
async def download_presentation(
    presentation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download a presentation file"""
    # Allow download for presentations created by user OR without user_id (markdown conversions)
    presentation = db.query(Presentation).filter(
        Presentation.id == presentation_id,
        Presentation.is_deleted == False
    ).filter(
        (Presentation.user_id == current_user.id) | (Presentation.user_id == None)
    ).first()
    
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation not found"
        )
    
    if not presentation.file_path or not os.path.exists(presentation.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation file not found"
        )
    
    return FileResponse(
        path=presentation.file_path,
        filename=f"{presentation.title}.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

@router.delete("/{presentation_id}")
async def delete_presentation(
    presentation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a presentation (soft delete)"""
    presentation = db.query(Presentation).filter(
        Presentation.id == presentation_id,
        Presentation.user_id == current_user.id,
        Presentation.is_deleted == False
    ).first()
    
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation not found"
        )
    
    presentation.is_deleted = True
    db.commit()
    
    app_logger.info(f"Presentation {presentation_id} deleted by user {current_user.username}")
    
    return {"message": "Presentation deleted successfully"}

@router.get("/stats/me", response_model=PresentationStats)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's presentation statistics"""
    # Total presentations
    total = db.query(func.count(Presentation.id)).filter(
        Presentation.user_id == current_user.id,
        Presentation.is_deleted == False
    ).scalar()
    
    # This month's presentations
    month_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly = db.query(func.count(Presentation.id)).filter(
        Presentation.user_id == current_user.id,
        Presentation.created_at >= month_start,
        Presentation.is_deleted == False
    ).scalar()
    
    # Total slides
    total_slides = db.query(func.sum(Presentation.slide_count)).filter(
        Presentation.user_id == current_user.id,
        Presentation.is_deleted == False
    ).scalar() or 0
    
    # Average slides
    avg_slides = total_slides / total if total > 0 else 0
    
    # Storage calculation (simplified)
    storage_mb = total * 2.5  # Assume average 2.5MB per presentation
    
    return PresentationStats(
        total_presentations=total,
        presentations_this_month=monthly,
        total_slides=total_slides,
        average_slides_per_presentation=avg_slides,
        storage_used_mb=storage_mb
    )

@router.get("/quota/me", response_model=UserQuota)
async def get_user_quota(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's quota information"""
    # Today's usage
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_used = db.query(func.count(Presentation.id)).filter(
        Presentation.user_id == current_user.id,
        Presentation.created_at >= today_start
    ).scalar()
    
    # Storage calculation
    total_presentations = db.query(func.count(Presentation.id)).filter(
        Presentation.user_id == current_user.id,
        Presentation.is_deleted == False
    ).scalar()
    storage_used = total_presentations * 2.5  # Simplified calculation
    
    return UserQuota(
        daily_limit=current_user.daily_ppt_limit,
        daily_used=today_used,
        remaining_today=max(0, current_user.daily_ppt_limit - today_used),
        storage_limit_mb=current_user.storage_limit_mb,
        storage_used_mb=storage_used,
        is_premium=current_user.role.value in ["premium", "admin"]
    )