"""
Markdown upload and conversion API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
import os
import tempfile
from datetime import datetime

from app.core.database import get_db
from app.core.logging import app_logger
from app.api.deps import get_current_user, get_current_verified_user
from app.models import User
from app.services import PPTGenerator, SlideContent, PresentationMetadata
from app.services.markdown_parser import parse_markdown_to_slides
from app.services.ai_service import get_ai_service

router = APIRouter(
    prefix="/api/v1/markdown",
    tags=["markdown"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload")
async def upload_markdown(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    template: Optional[str] = Form("McKinsey Professional"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Upload markdown file and convert to PPT
    
    Args:
        file: Markdown file (.md)
        title: Optional presentation title
        template: Template name to use
        
    Returns:
        Presentation details with download URL
    """
    try:
        # Validate file extension
        if not file.filename.endswith('.md'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only markdown files (.md) are supported"
            )
        
        # Read markdown content
        content = await file.read()
        markdown_text = content.decode('utf-8')
        
        # Parse markdown to slides
        slides_data = parse_markdown_to_slides(markdown_text)
        
        if not slides_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not parse any slides from the markdown content"
            )
        
        # Convert to SlideContent objects
        slides = []
        for slide_data in slides_data:
            slide = SlideContent(
                title=slide_data.get("title", ""),
                content=slide_data.get("content", []),
                layout_type=slide_data.get("layout_type", "content"),
                speaker_notes=slide_data.get("speaker_notes", ""),
                charts=slide_data.get("charts", []),
                tables=slide_data.get("tables", []),
                images=slide_data.get("images", [])
            )
            slides.append(slide)
        
        # Create presentation metadata
        presentation_title = title or file.filename.replace('.md', '')
        metadata = PresentationMetadata(
            title=presentation_title,
            author=current_user.full_name or current_user.username,
            subject="Converted from Markdown",
            category="Markdown Import"
        )
        
        # Generate PPT
        generator = PPTGenerator(db)
        file_path, presentation_model = generator.create_presentation(
            slides_content=slides,
            metadata=metadata,
            template_name=template,
            save_to_db=True
        )
        
        if not file_path or not presentation_model:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate presentation"
            )
        
        app_logger.info(f"Markdown converted to PPT: {presentation_model.id} for user {current_user.username}")
        
        return {
            "success": True,
            "presentation_id": str(presentation_model.id),
            "title": presentation_model.title,
            "slide_count": presentation_model.slide_count,
            "download_url": f"/api/v1/presentations/{presentation_model.id}/download",
            "message": f"Successfully converted {len(slides)} slides from markdown"
        }
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File encoding not supported. Please use UTF-8 encoded markdown files"
        )
    except Exception as e:
        app_logger.error(f"Error converting markdown: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to convert markdown: {str(e)}"
        )


@router.post("/convert")
async def convert_markdown_text(
    markdown_content: str = Form(...),
    title: str = Form(...),
    template: Optional[str] = Form("McKinsey Professional"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Convert markdown text to PPT
    
    Args:
        markdown_content: Markdown text content
        title: Presentation title
        template: Template name to use
        
    Returns:
        Presentation details with download URL
    """
    try:
        # Get AI service for content enhancement
        ai_service = get_ai_service()
        
        # Enhance markdown content with AI if available
        enhanced_markdown = await ai_service.enhance_markdown_content(
            markdown_content,
            context={"title": title, "template": template}
        )
        
        # Parse markdown to slides (use enhanced version if available)
        slides_data = parse_markdown_to_slides(enhanced_markdown)
        
        if not slides_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not parse any slides from the markdown content"
            )
        
        # Convert to SlideContent objects and improve with AI
        slides = []
        for slide_data in slides_data:
            # Improve individual slide content with AI
            improved_slide = await ai_service.improve_slide_content(slide_data)
            
            slide = SlideContent(
                title=improved_slide.get("title", ""),
                content=improved_slide.get("content", []),
                layout_type=improved_slide.get("layout_type", "content"),
                speaker_notes=improved_slide.get("speaker_notes", ""),
                charts=improved_slide.get("charts", []),
                tables=improved_slide.get("tables", []),
                images=improved_slide.get("images", [])
            )
            slides.append(slide)
        
        # Create presentation metadata
        metadata = PresentationMetadata(
            title=title,
            author=current_user.full_name or current_user.username,
            subject="Converted from Markdown",
            category="Markdown Import"
        )
        
        # Generate PPT
        generator = PPTGenerator(db)
        file_path, presentation_model = generator.create_presentation(
            slides_content=slides,
            metadata=metadata,
            template_name=template,
            save_to_db=True
        )
        
        if not file_path or not presentation_model:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate presentation"
            )
        
        app_logger.info(f"Markdown text converted to PPT: {presentation_model.id}")
        
        return {
            "success": True,
            "presentation_id": str(presentation_model.id),
            "title": presentation_model.title,
            "slide_count": presentation_model.slide_count,
            "download_url": f"/api/v1/presentations/{presentation_model.id}/download",
            "message": f"Successfully converted {len(slides)} slides from markdown"
        }
        
    except Exception as e:
        app_logger.error(f"Error converting markdown text: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to convert markdown: {str(e)}"
        )


@router.get("/sample")
async def get_sample_markdown():
    """
    Get sample markdown for testing
    
    Returns:
        Sample markdown content with examples
    """
    sample = """# Digital Transformation Strategy
## Executive Presentation for C-Suite

---

## Executive Summary

### Key Findings
- Digital transformation is critical for competitive advantage
- 75% of industry leaders have begun transformation initiatives
- Expected ROI of 35% within 3 years
- Customer experience improvement of 40%

> Speaker note: Emphasize the urgency and competitive pressure

---

## Market Analysis

### Current Market Size
- Global market: $2.3 trillion
- Annual growth rate: 16.5%
- Key players capturing 60% market share

### Growth Projections

```chart
type: column
title: Market Growth Projection
categories: [2023, 2024, 2025, 2026]
series:
  - name: Market Size (Trillion $)
    values: [2.3, 2.7, 3.1, 3.6]
```

---

## Strategic Pillars

### 1. Customer Experience
- Omnichannel integration
- Personalization at scale
- Real-time engagement

### 2. Operational Excellence
- Process automation
- Data-driven decision making
- Agile methodology adoption

### 3. Innovation Ecosystem
- Partnership networks
- Innovation labs
- Startup collaboration

---

## Implementation Roadmap

| Phase | Timeline | Key Initiatives | Investment |
|-------|----------|----------------|------------|
| Foundation | Q1-Q2 2024 | Infrastructure modernization | $5M |
| Transformation | Q3-Q4 2024 | Process digitization | $8M |
| Scale | 2025 | Full deployment | $12M |
| Optimize | 2026+ | Continuous improvement | $3M/year |

---

## Expected Outcomes

### Financial Impact
- Revenue increase: 25%
- Cost reduction: 15%
- Productivity gain: 30%

### Customer Impact
- NPS improvement: +20 points
- Customer retention: +15%
- Digital engagement: 3x

> Speaker note: These are conservative estimates based on industry benchmarks

---

## Next Steps

1. **Board approval** for transformation initiative
2. **Establish transformation office** with dedicated team
3. **Select technology partners** through RFP process
4. **Launch pilot programs** in Q1 2024
5. **Develop change management** program

---

## Questions & Discussion

Thank you for your attention.

Contact: transformation@company.com
"""
    
    return {
        "sample_markdown": sample,
        "instructions": "Save this content as a .md file and upload it, or paste directly into the convert endpoint",
        "markdown_rules": {
            "title_slide": "# Main Title",
            "section_slide": "## Section Title",
            "content_slide": "### Slide Title with bullet points",
            "slide_break": "--- (three dashes)",
            "speaker_notes": "> Note text (blockquote)",
            "table": "Use markdown table syntax",
            "chart": "Use code block with 'chart' label"
        }
    }