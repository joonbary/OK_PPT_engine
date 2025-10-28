# PPT Generation Services

Comprehensive PowerPoint generation services for creating professional McKinsey-style presentations with python-pptx.

## Overview

This module provides three main services:

1. **PPTGenerator** - Main presentation generation engine
2. **TemplateManager** - Template creation and management
3. **McKinseyStyles** - Professional styling and formatting

## Features

- ✅ Multiple slide layouts (title, content, two-column, chart, table, image)
- ✅ McKinsey-style professional formatting
- ✅ Chart generation with data visualization
- ✅ Table creation with custom styling
- ✅ Image integration and positioning
- ✅ Speaker notes support
- ✅ Template management system
- ✅ Database integration for metadata tracking
- ✅ Error handling and logging
- ✅ File system management

## Quick Start

```python
from app.services import PPTGenerator, SlideContent, PresentationMetadata

# Initialize generator
generator = PPTGenerator(db_session)

# Create slide content
slides = [
    SlideContent(
        title="Executive Summary",
        content=["Key finding 1", "Key finding 2", "Key finding 3"],
        layout_type="content"
    )
]

# Create metadata
metadata = PresentationMetadata(
    title="Strategic Initiative",
    author="McKinsey & Company"
)

# Generate presentation
file_path, presentation_model = generator.create_presentation(
    slides_content=slides,
    metadata=metadata,
    template_name="McKinsey Professional"
)
```

## Service Documentation

### PPTGenerator

Main class for creating PowerPoint presentations.

#### Key Methods

```python
create_presentation(slides_content, metadata, template_name, save_to_db)
```
Creates a complete presentation with multiple slides.

```python
load_presentation_from_file(file_path)
```
Loads existing presentation from file system.

```python
update_slide_content(presentation, slide_index, new_content)
```
Updates content of a specific slide.

```python
get_presentation_info(file_path)
```
Retrieves metadata and information about a presentation file.

#### SlideContent Structure

```python
@dataclass
class SlideContent:
    title: str = ""
    subtitle: str = ""
    content: List[str] = None
    layout_type: str = "content"
    images: List[str] = None
    charts: List[Dict[str, Any]] = None
    tables: List[Dict[str, Any]] = None
    speaker_notes: str = ""
```

#### PresentationMetadata Structure

```python
@dataclass
class PresentationMetadata:
    title: str
    author: str = ""
    subject: str = ""
    category: str = ""
    creation_time: datetime = None
    slide_count: int = 0
    word_count: int = 0
    generation_time: float = 0.0
    ai_model: str = ""
    ai_tokens_used: int = 0
```

### TemplateManager

Handles template creation, management, and application.

#### Key Methods

```python
create_template(config: TemplateConfig)
```
Creates a new template with specified configuration.

```python
get_template_by_name(name: str)
```
Retrieves template by name.

```python
list_templates(category: str = None)
```
Lists available templates, optionally filtered by category.

```python
apply_template_to_presentation(presentation, template)
```
Applies template styling to an existing presentation.

#### TemplateConfig Structure

```python
@dataclass
class TemplateConfig:
    name: str
    description: str
    category: str
    colors: Dict[str, Any]
    fonts: Dict[str, Any]
    layouts: Dict[str, Any]
    chart_style: Dict[str, Any]
    table_style: Dict[str, Any]
    metadata: Dict[str, Any] = None
```

### McKinseyStyles

Professional styling and formatting specifications.

#### Available Classes

- **McKinseyColors** - Brand colors and professional palette
- **McKinseyFonts** - Font specifications and formatting
- **McKinseyLayouts** - Slide layout dimensions and positioning

#### Layout Types

- `title` - Title slide with main title and subtitle
- `content` - Content slide with bullet points
- `two_column` - Two-column layout for comparisons
- `chart` - Chart slide with data visualization
- `table` - Table slide with structured data
- `image` - Image slide with pictures and captions
- `blank` - Blank slide for custom content
- `section_header` - Section divider slide

## Usage Examples

### Creating Different Slide Types

#### Title Slide
```python
title_slide = SlideContent(
    title="Strategic Initiative Overview",
    subtitle="McKinsey & Company Professional Template",
    layout_type="title"
)
```

#### Content Slide with Bullet Points
```python
content_slide = SlideContent(
    title="Key Findings",
    content=[
        "Market opportunity of $2.5B identified",
        "Three-phase implementation strategy",
        "Expected ROI of 300% within 24 months"
    ],
    layout_type="content",
    speaker_notes="Emphasize the strong business case"
)
```

#### Chart Slide
```python
chart_slide = SlideContent(
    title="Market Growth Projection",
    layout_type="chart",
    charts=[{
        "type": "column",
        "title": "Revenue Growth (2023-2026)",
        "categories": ["2023", "2024", "2025", "2026"],
        "series": [{
            "name": "Revenue ($M)",
            "values": [100, 150, 225, 340]
        }]
    }]
)
```

#### Table Slide
```python
table_slide = SlideContent(
    title="Implementation Timeline",
    layout_type="table",
    tables=[{
        "headers": ["Phase", "Duration", "Key Activities", "Investment"],
        "rows": [
            ["Phase 1", "Months 1-6", "Foundation setup", "$2.5M"],
            ["Phase 2", "Months 7-12", "Development", "$4.2M"],
            ["Phase 3", "Months 13-18", "Deployment", "$3.8M"]
        ]
    }]
)
```

#### Two-Column Comparison
```python
comparison_slide = SlideContent(
    title="Current vs Future State",
    content=[
        "Current Challenges:",
        "• Legacy systems",
        "• Manual processes",
        "• Limited analytics",
        "Future Vision:",
        "• Cloud-native architecture", 
        "• Automated workflows",
        "• Advanced analytics"
    ],
    layout_type="two_column"
)
```

### Chart Types Supported

- **Column Charts** - `type: "column"`
- **Line Charts** - `type: "line"`
- **Pie Charts** - `type: "pie"`
- **Bar Charts** - `type: "bar"`

### Chart Data Format

```python
chart_data = {
    "type": "column",
    "title": "Chart Title",
    "categories": ["Q1", "Q2", "Q3", "Q4"],
    "series": [{
        "name": "Series 1",
        "values": [10, 20, 30, 40]
    }, {
        "name": "Series 2", 
        "values": [15, 25, 35, 45]
    }]
}
```

### Custom Template Creation

```python
from app.services import TemplateManager, TemplateConfig
from app.services.mckinsey_styles import McKinseyColors, McKinseyFonts

# Create custom template configuration
config = TemplateConfig(
    name="Custom Professional",
    description="Custom professional template",
    category="Business",
    colors={
        "primary": McKinseyColors.PRIMARY_BLUE,
        "secondary": McKinseyColors.SECONDARY_BLUE,
        "background": McKinseyColors.WHITE
    },
    fonts={
        "primary": McKinseyFonts.PRIMARY_FONT,
        "title_size": McKinseyFonts.TITLE_SIZE,
        "body_size": McKinseyFonts.BODY_SIZE
    },
    layouts={},  # Use default layouts
    chart_style={},  # Use default chart styling
    table_style={}   # Use default table styling
)

# Create template
template_manager = TemplateManager(db_session)
template = template_manager.create_template(config)
```

## Error Handling

All services include comprehensive error handling:

```python
try:
    file_path, presentation = generator.create_presentation(slides, metadata)
    if file_path:
        print(f"Success: {file_path}")
    else:
        print("Failed to create presentation")
except Exception as e:
    logger.error(f"Generation error: {e}")
```

## Logging

Services use Python logging for monitoring and debugging:

```python
import logging
logger = logging.getLogger(__name__)

# Configure logging level
logging.basicConfig(level=logging.INFO)
```

## File Management

Generated presentations are saved to the configured output directory:

```python
# Default: output/presentations/
# Custom: PPTGenerator(db, output_dir="custom/path")
```

Files are named with timestamp and clean title:
- `Strategic_Initiative_20231201_143022.pptx`

## Database Integration

Presentations can be saved to database with full metadata:

```python
# Enable database saving
file_path, presentation_model = generator.create_presentation(
    slides_content=slides,
    metadata=metadata,
    save_to_db=True  # Creates database records
)

# Access presentation ID
print(f"Presentation ID: {presentation_model.id}")
```

## Performance Considerations

- **Memory Usage**: Large presentations with many images/charts
- **Generation Time**: Typically 2-5 seconds for 10-slide presentation
- **File Size**: 500KB-2MB depending on content
- **Concurrent Generation**: Thread-safe for multiple requests

## Dependencies

Required packages (included in requirements.txt):
- `python-pptx==0.6.21` - PowerPoint generation
- `Pillow==10.1.0` - Image processing
- `sqlalchemy==2.0.23` - Database integration

## Testing

Run the example script to test functionality:

```bash
python app/services/example_usage.py
```

This will create a sample presentation demonstrating all features.

## Integration with FastAPI

Example API endpoint:

```python
from fastapi import APIRouter, Depends
from app.services import PPTGenerator, SlideContent, PresentationMetadata

@router.post("/generate")
async def generate_presentation(
    request: PresentationRequest,
    db: Session = Depends(get_db)
):
    generator = PPTGenerator(db)
    
    # Convert request to slide content
    slides = [
        SlideContent(**slide_data) 
        for slide_data in request.slides
    ]
    
    metadata = PresentationMetadata(
        title=request.title,
        author=request.author
    )
    
    # Generate presentation
    file_path, presentation = generator.create_presentation(
        slides_content=slides,
        metadata=metadata
    )
    
    return {
        "file_path": file_path,
        "presentation_id": presentation.id if presentation else None
    }
```

## Customization

### Custom Slide Layouts

Extend the layout system by:
1. Adding new `SlideLayoutType` enum values
2. Implementing layout logic in `PPTGenerator._create_slide()`
3. Adding layout configuration in `McKinseyStyles.get_layout_config()`

### Custom Styling

Override McKinsey styles by:
1. Creating custom color schemes in `McKinseyColors`
2. Defining new font specifications in `McKinseyFonts`
3. Modifying layout dimensions in `McKinseyLayouts`

### Additional Chart Types

Add new chart types by:
1. Extending chart data format
2. Adding chart type mapping in `_add_chart_to_slide()`
3. Implementing chart-specific styling

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies installed
2. **File Permissions**: Check output directory write permissions
3. **Chart Generation**: Verify chart data format and values
4. **Image Loading**: Confirm image files exist and are accessible
5. **Template Not Found**: Verify template exists in database

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

For large presentations:
- Reduce image sizes before adding
- Limit chart data points
- Use efficient slide layouts
- Consider batch processing

## Future Enhancements

Planned improvements:
- PDF export functionality
- Animation support
- Advanced chart types
- Master slide customization
- Bulk presentation generation
- Template marketplace
- Real-time collaboration features