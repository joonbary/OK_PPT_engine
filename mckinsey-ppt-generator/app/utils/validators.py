"""
Validation utilities for the PPT generation system
"""

import re
from typing import Any, Dict, List, Optional
from datetime import datetime


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> Dict[str, Any]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        Dictionary with validation result and messages
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one digit")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "strength": calculate_password_strength(password)
    }


def calculate_password_strength(password: str) -> str:
    """
    Calculate password strength
    
    Args:
        password: Password to analyze
        
    Returns:
        Strength level: weak, medium, strong, very_strong
    """
    score = 0
    
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    
    if score <= 2:
        return "weak"
    elif score == 3:
        return "medium"
    elif score == 4:
        return "strong"
    else:
        return "very_strong"


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate file extension
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions
        
    Returns:
        True if extension is allowed, False otherwise
    """
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions


def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    """
    Validate date range
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        True if valid date range, False otherwise
    """
    return start_date <= end_date


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove any path components
    filename = filename.replace('/', '').replace('\\', '')
    
    # Remove special characters except dots and underscores
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = 250 - len(ext)
        filename = f"{name[:max_name_length]}.{ext}" if ext else name[:255]
    
    return filename


def validate_slide_count(count: int) -> Dict[str, Any]:
    """
    Validate slide count
    
    Args:
        count: Number of slides requested
        
    Returns:
        Validation result
    """
    min_slides = 3
    max_slides = 50
    optimal_range = (5, 20)
    
    if count < min_slides:
        return {
            "valid": False,
            "error": f"Minimum {min_slides} slides required"
        }
    
    if count > max_slides:
        return {
            "valid": False,
            "error": f"Maximum {max_slides} slides allowed"
        }
    
    return {
        "valid": True,
        "is_optimal": optimal_range[0] <= count <= optimal_range[1],
        "message": "Slide count is valid"
    }