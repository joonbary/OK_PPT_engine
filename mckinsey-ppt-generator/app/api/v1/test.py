from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging import app_logger
from app.models import Presentation, PresentationStatus, PresentationType
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/api/v1/test",
    tags=["test"],
    responses={404: {"description": "Not found"}},
)

@router.get("/logging")
async def test_logging():
    """Test logging at different levels"""
    app_logger.debug("This is a DEBUG message")
    app_logger.info("This is an INFO message")
    app_logger.warning("This is a WARNING message")
    app_logger.error("This is an ERROR message")
    
    return {
        "message": "Logging test completed",
        "log_files": ["logs/app.log", "logs/error.log", "logs/api.log"]
    }

@router.get("/database")
async def test_database(db: Session = Depends(get_db)):
    """Test database connection"""
    try:
        # Create a test presentation
        test_presentation = Presentation(
            title="Test Presentation",
            description="This is a test presentation",
            type=PresentationType.CUSTOM,
            status=PresentationStatus.DRAFT,
            user_email="test@example.com",
            presentation_metadata={"test": True},
            slide_count=0,
        )
        
        # Add to database
        db.add(test_presentation)
        db.commit()
        db.refresh(test_presentation)
        
        # Query from database
        result = db.query(Presentation).filter(
            Presentation.id == test_presentation.id
        ).first()
        
        # Clean up
        db.delete(result)
        db.commit()
        
        app_logger.info(f"Database test successful: Created and deleted presentation {test_presentation.id}")
        
        return {
            "status": "success",
            "message": "Database connection and operations working",
            "test_id": str(test_presentation.id)
        }
        
    except Exception as e:
        app_logger.error(f"Database test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database test failed: {str(e)}")

@router.get("/error")
async def test_error_handling():
    """Test error handling"""
    app_logger.warning("Testing error handling endpoint")
    raise HTTPException(status_code=400, detail="This is a test error")

@router.get("/exception")
async def test_exception():
    """Test unexpected exception handling"""
    app_logger.warning("Testing unexpected exception")
    # This will cause an unexpected exception
    result = 1 / 0
    return {"result": result}