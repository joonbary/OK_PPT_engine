"""
Markdown to PPT Slide Parser

Converts markdown documents into structured slide content for PPT generation.
Supports various markdown elements and McKinsey-style formatting.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from loguru import logger


@dataclass
class ParsedSlide:
    """Parsed slide content from markdown"""
    title: str
    content: List[str]
    layout_type: str
    level: int
    charts: List[Dict[str, Any]] = None
    tables: List[Dict[str, Any]] = None
    images: List[str] = None
    speaker_notes: str = ""
    
    def __post_init__(self):
        if self.charts is None:
            self.charts = []
        if self.tables is None:
            self.tables = []
        if self.images is None:
            self.images = []


class MarkdownParser:
    """
    Parser for converting markdown to slide structure
    
    Markdown Rules:
    - # Title -> Title slide
    - ## Section -> New section slide
    - ### Subsection -> Content slide
    - #### Point -> Sub-points in content
    - Bullet lists -> Content points
    - Tables -> Table slides
    - Code blocks with chart -> Chart slides
    - Images -> Image slides
    - > Blockquote -> Speaker notes
    - --- -> Slide break
    """
    
    def __init__(self):
        self.logger = logger.bind(service="MarkdownParser")
        
    def parse(self, markdown_content: str) -> List[ParsedSlide]:
        """
        Parse markdown content into slides
        
        Args:
            markdown_content: Raw markdown text
            
        Returns:
            List of parsed slides
        """
        try:
            slides = []
            
            # Split by slide markers (---, ===, or double newline + heading)
            sections = self._split_into_sections(markdown_content)
            
            for section in sections:
                if not section.strip():
                    continue
                    
                slide = self._parse_section(section)
                if slide:
                    slides.append(slide)
            
            # If no slides were created, create from content
            if not slides and markdown_content.strip():
                slides = self._create_slides_from_content(markdown_content)
            
            self.logger.info(f"Parsed {len(slides)} slides from markdown")
            return slides
            
        except Exception as e:
            self.logger.error(f"Error parsing markdown: {e}")
            return []
    
    def _split_into_sections(self, content: str) -> List[str]:
        """
        Split markdown into sections by slide markers
        """
        # Split by horizontal rules (--- or ***)
        sections = re.split(r'\n(?:---|===|\*\*\*)\n', content)
        
        # If no explicit breaks, split by top-level headers
        if len(sections) == 1:
            # Split by # or ## headers
            sections = re.split(r'\n(?=#+ )', content)
        
        return sections
    
    def _parse_section(self, section: str) -> Optional[ParsedSlide]:
        """
        Parse a section into a slide
        """
        lines = section.strip().split('\n')
        if not lines:
            return None
        
        slide = ParsedSlide(
            title="",
            content=[],
            layout_type="content",
            level=1
        )
        
        # Extract speaker notes (blockquotes)
        lines, speaker_notes = self._extract_speaker_notes(lines)
        slide.speaker_notes = speaker_notes
        
        # Parse title from heading
        title, level, remaining_lines = self._extract_title(lines)
        slide.title = title
        slide.level = level
        
        # Determine slide type and parse content
        if self._contains_table(remaining_lines):
            slide.layout_type = "table"
            slide.tables = [self._parse_table(remaining_lines)]
        elif self._contains_chart(remaining_lines):
            slide.layout_type = "chart"
            slide.charts = [self._parse_chart(remaining_lines)]
        elif self._contains_image(remaining_lines):
            slide.layout_type = "image"
            slide.images = self._extract_images(remaining_lines)
        else:
            # Parse as content slide
            slide.content = self._parse_content(remaining_lines)
            
            # Determine layout based on content
            if level == 1 and len(slide.content) == 0:
                slide.layout_type = "title"
            elif len(slide.content) > 6:
                slide.layout_type = "two_column"
            else:
                slide.layout_type = "content"
        
        return slide
    
    def _extract_title(self, lines: List[str]) -> Tuple[str, int, List[str]]:
        """
        Extract title from heading
        
        Returns:
            (title, heading_level, remaining_lines)
        """
        for i, line in enumerate(lines):
            if line.startswith('#'):
                # Count heading level
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                return title, level, lines[i+1:]
        
        # No heading found, use first line as title
        if lines:
            return lines[0], 3, lines[1:]
        
        return "", 3, []
    
    def _extract_speaker_notes(self, lines: List[str]) -> Tuple[List[str], str]:
        """
        Extract speaker notes from blockquotes
        """
        notes = []
        remaining = []
        
        for line in lines:
            if line.strip().startswith('>'):
                notes.append(line.strip().lstrip('>').strip())
            else:
                remaining.append(line)
        
        return remaining, '\n'.join(notes)
    
    def _parse_content(self, lines: List[str]) -> List[str]:
        """
        Parse content from lines
        """
        content = []
        current_item = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_item:
                    content.append(' '.join(current_item))
                    current_item = []
                continue
            
            # Handle bullet points
            if line.startswith(('- ', '* ', '+ ', '• ')):
                if current_item:
                    content.append(' '.join(current_item))
                    current_item = []
                content.append(line.lstrip('- *+•').strip())
            # Handle numbered lists
            elif re.match(r'^\d+\.?\s+', line):
                if current_item:
                    content.append(' '.join(current_item))
                    current_item = []
                content.append(re.sub(r'^\d+\.?\s+', '', line))
            # Continue previous item or start new paragraph
            else:
                if line.startswith('  '):
                    # Sub-item
                    if content:
                        content[-1] += f"\n  {line.strip()}"
                else:
                    current_item.append(line)
        
        # Add any remaining item
        if current_item:
            content.append(' '.join(current_item))
        
        return content
    
    def _contains_table(self, lines: List[str]) -> bool:
        """
        Check if lines contain a markdown table
        """
        for line in lines:
            if '|' in line and '-' in line:
                return True
        return False
    
    def _parse_table(self, lines: List[str]) -> Dict[str, Any]:
        """
        Parse markdown table
        """
        table_lines = []
        for line in lines:
            if '|' in line:
                table_lines.append(line)
        
        if len(table_lines) < 2:
            return {}
        
        # Parse headers
        headers = [cell.strip() for cell in table_lines[0].split('|') if cell.strip()]
        
        # Skip separator line
        rows = []
        for line in table_lines[2:]:
            row = [cell.strip() for cell in line.split('|') if cell.strip()]
            if row:
                rows.append(row)
        
        return {
            "headers": headers,
            "rows": rows
        }
    
    def _contains_chart(self, lines: List[str]) -> bool:
        """
        Check if lines contain chart definition (in code block)
        """
        in_code_block = False
        for line in lines:
            if line.strip().startswith('```'):
                if 'chart' in line.lower() or 'graph' in line.lower():
                    return True
                in_code_block = not in_code_block
            elif in_code_block and any(word in line.lower() for word in ['chart:', 'type:', 'data:']):
                return True
        return False
    
    def _parse_chart(self, lines: List[str]) -> Dict[str, Any]:
        """
        Parse chart definition from code block
        
        Example:
        ```chart
        type: bar
        title: Sales Growth
        categories: [Q1, Q2, Q3, Q4]
        series:
          - name: Revenue
            values: [100, 120, 140, 160]
        ```
        """
        chart_data = {
            "type": "column",
            "title": "Chart",
            "categories": [],
            "series": []
        }
        
        in_chart_block = False
        chart_text = []
        
        for line in lines:
            if line.strip().startswith('```'):
                if 'chart' in line.lower():
                    in_chart_block = True
                elif in_chart_block:
                    break
            elif in_chart_block:
                chart_text.append(line)
        
        # Simple parsing of chart definition
        for line in chart_text:
            if 'type:' in line:
                chart_data['type'] = line.split('type:')[1].strip()
            elif 'title:' in line:
                chart_data['title'] = line.split('title:')[1].strip()
            elif 'categories:' in line:
                # Parse list
                cat_str = line.split('categories:')[1].strip()
                if cat_str.startswith('[') and cat_str.endswith(']'):
                    chart_data['categories'] = [c.strip().strip('"\'') for c in cat_str[1:-1].split(',')]
        
        # If no chart data found, create sample data
        if not chart_data['categories']:
            chart_data = {
                "type": "column",
                "title": "Data Visualization",
                "categories": ["Category 1", "Category 2", "Category 3", "Category 4"],
                "series": [{
                    "name": "Series 1",
                    "values": [25, 40, 30, 35]
                }]
            }
        
        return chart_data
    
    def _contains_image(self, lines: List[str]) -> bool:
        """
        Check if lines contain image references
        """
        for line in lines:
            if re.search(r'!\[.*?\]\(.*?\)', line):
                return True
        return False
    
    def _extract_images(self, lines: List[str]) -> List[str]:
        """
        Extract image URLs from markdown
        """
        images = []
        for line in lines:
            # Find markdown images ![alt](url)
            matches = re.findall(r'!\[.*?\]\((.*?)\)', line)
            images.extend(matches)
        return images
    
    def _create_slides_from_content(self, content: str) -> List[ParsedSlide]:
        """
        Create slides from content when no structure is found
        """
        slides = []
        
        # Create title slide
        lines = content.strip().split('\n')
        if lines:
            slides.append(ParsedSlide(
                title=lines[0][:100],  # First line as title
                content=[],
                layout_type="title",
                level=1
            ))
        
        # Create content slides from remaining text
        if len(lines) > 1:
            # Group content into slides (max 5 points per slide)
            content_points = []
            for line in lines[1:]:
                if line.strip():
                    content_points.append(line.strip())
            
            # Create slides with max 5 points each
            for i in range(0, len(content_points), 5):
                slide_content = content_points[i:i+5]
                slides.append(ParsedSlide(
                    title=f"Content {(i//5) + 1}",
                    content=slide_content,
                    layout_type="content",
                    level=2
                ))
        
        return slides


def parse_markdown_to_slides(markdown_content: str) -> List[Dict[str, Any]]:
    """
    Convenience function to parse markdown to slide dictionaries
    
    Args:
        markdown_content: Raw markdown text
        
    Returns:
        List of slide dictionaries ready for PPT generation
    """
    parser = MarkdownParser()
    parsed_slides = parser.parse(markdown_content)
    
    slides = []
    for ps in parsed_slides:
        slide = {
            "title": ps.title,
            "content": ps.content,
            "layout_type": ps.layout_type,
            "speaker_notes": ps.speaker_notes
        }
        
        if ps.charts:
            slide["charts"] = ps.charts
        if ps.tables:
            slide["tables"] = ps.tables
        if ps.images:
            slide["images"] = ps.images
        
        slides.append(slide)
    
    return slides