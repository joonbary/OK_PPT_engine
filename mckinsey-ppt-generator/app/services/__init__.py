"""
Services module for PowerPoint generation.

This module provides comprehensive services for generating professional
PowerPoint presentations with McKinsey-style formatting and templates.
"""

from .ppt_generator import PPTGenerator, SlideContent, PresentationMetadata
from .template_manager import TemplateManager, TemplateConfig
from .mckinsey_styles import (
    McKinseyStyles, 
    McKinseyColors, 
    McKinseyFonts, 
    McKinseyLayouts,
    SlideLayoutType,
    create_mckinsey_template
)
from .markdown_parser import MarkdownParser, parse_markdown_to_slides

__all__ = [
    "PPTGenerator",
    "SlideContent", 
    "PresentationMetadata",
    "TemplateManager",
    "TemplateConfig",
    "McKinseyStyles",
    "McKinseyColors",
    "McKinseyFonts", 
    "McKinseyLayouts",
    "SlideLayoutType",
    "create_mckinsey_template",
    "MarkdownParser",
    "parse_markdown_to_slides"
]