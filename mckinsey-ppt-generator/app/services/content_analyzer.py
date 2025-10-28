"""
Content Analyzer for optimizing slide layouts based on content type.
Analyzes markdown content to determine the best layout for each slide.
"""

import re
from typing import Dict, List, Optional, Any
from app.core.logging import app_logger


class ContentAnalyzer:
    """
    마크다운 콘텐츠를 분석하여 최적 레이아웃 결정
    """
    
    def __init__(self):
        """Initialize content analyzer with detection patterns"""
        self.bullet_pattern = re.compile(r'^[\s]*[\*\-\+•]\s+', re.MULTILINE)
        self.table_pattern = re.compile(r'\|.*\|.*\|', re.MULTILINE)
        self.image_pattern = re.compile(r'!\[.*?\]\(.*?\)')
        self.chart_pattern = re.compile(r'(?:chart|graph|diagram|matrix)', re.IGNORECASE)
        self.comparison_keywords = ['vs', 'versus', '대비', '비교', 'before', 'after', '이전', '이후']
        
    def analyze_slide_content(self, markdown_content: str, slide_title: str = "") -> Dict[str, Any]:
        """
        콘텐츠 분석 후 레이아웃 추천
        
        Returns:
        {
            "content_type": "list" | "comparison" | "matrix" | "image_text" | "title_only" | "paragraph",
            "complexity": "simple" | "medium" | "complex",
            "element_count": int,
            "has_chart": bool,
            "has_image": bool,
            "has_table": bool,
            "text_density": "low" | "medium" | "high",
            "bullet_count": int,
            "recommended_layout": "layout_name"
        }
        """
        try:
            # Initialize analysis results
            analysis = {
                "content_type": "paragraph",
                "complexity": "simple",
                "element_count": 0,
                "has_chart": False,
                "has_image": False,
                "has_table": False,
                "text_density": "low",
                "bullet_count": 0,
                "recommended_layout": "single_column"
            }
            
            # Detect content type
            content_type = self.detect_content_type(markdown_content, slide_title)
            analysis["content_type"] = content_type
            
            # Count elements
            bullet_count = len(self.bullet_pattern.findall(markdown_content))
            analysis["bullet_count"] = bullet_count
            analysis["element_count"] = bullet_count
            
            # Detect special elements
            analysis["has_table"] = bool(self.table_pattern.search(markdown_content))
            analysis["has_image"] = bool(self.image_pattern.search(markdown_content))
            analysis["has_chart"] = bool(self.chart_pattern.search(markdown_content)) or analysis["has_table"]
            
            # Calculate text density
            analysis["text_density"] = self.calculate_text_density(markdown_content)
            
            # Determine complexity
            if analysis["has_table"] or analysis["has_chart"] or bullet_count > 5:
                analysis["complexity"] = "complex"
            elif bullet_count > 3 or analysis["text_density"] == "high":
                analysis["complexity"] = "medium"
            else:
                analysis["complexity"] = "simple"
            
            # Recommend layout with enhanced detection
            analysis["recommended_layout"] = self.recommend_layout(analysis, markdown_content, slide_title)
            
            app_logger.info(f"Content analysis completed: {analysis['content_type']} -> {analysis['recommended_layout']}")
            return analysis
            
        except Exception as e:
            app_logger.error(f"Content analysis failed: {str(e)}")
            return {
                "content_type": "paragraph",
                "complexity": "simple",
                "element_count": 0,
                "has_chart": False,
                "has_image": False,
                "has_table": False,
                "text_density": "medium",
                "bullet_count": 0,
                "recommended_layout": "single_column"
            }
    
    def detect_content_type(self, markdown: str, title: str = "") -> str:
        """
        콘텐츠 타입 감지
        
        감지 규칙:
        - 3개 이상 불릿 포인트 → "list"
        - 비교 키워드 → "comparison" 
        - 표 또는 매트릭스 → "matrix"
        - 이미지 + 텍스트 → "image_text"
        - 짧은 텍스트만 → "title_only"
        - 긴 텍스트 → "paragraph"
        """
        # Check for title-only slides
        if len(markdown.strip()) < 50 and not self.bullet_pattern.search(markdown):
            return "title_only"
        
        # Check for matrix/table
        if self.table_pattern.search(markdown) or "matrix" in markdown.lower() or "매트릭스" in markdown:
            return "matrix"
        
        # Check for comparison
        combined_text = (title + " " + markdown).lower()
        if any(keyword in combined_text for keyword in self.comparison_keywords):
            return "comparison"
        
        # Check for image with text
        if self.image_pattern.search(markdown) or self.chart_pattern.search(markdown):
            return "image_text"
        
        # Check for bullet list
        bullet_count = len(self.bullet_pattern.findall(markdown))
        if bullet_count >= 3:
            return "list"
        elif bullet_count > 0:
            return "list"  # Even with fewer bullets, treat as list
        
        # Default to paragraph for longer text
        return "paragraph"
    
    def calculate_text_density(self, text: str) -> str:
        """
        텍스트 밀도 계산 (단어 수 기준)
        
        - low: < 50 단어
        - medium: 50-150 단어
        - high: > 150 단어
        """
        # Remove markdown syntax for accurate word count
        clean_text = re.sub(r'[#*\[\]()]', '', text)
        
        # Count words (works for both Korean and English)
        # Korean words are counted by spaces and particles
        words = clean_text.split()
        korean_chars = len(re.findall(r'[\u3131-\ucb4c]', clean_text))
        
        # Estimate Korean words (rough estimate: 2-3 chars per word)
        korean_words = korean_chars // 3 if korean_chars > 0 else 0
        total_words = max(len(words), korean_words)
        
        if total_words < 50:
            return "low"
        elif total_words < 150:
            return "medium"
        else:
            return "high"
    
    def recommend_layout(self, analysis: Dict[str, Any], content_text: str = "", title: str = "") -> str:
        """
        Enhanced layout recommendation using LayoutLibrary's advanced selection
        """
        from app.services.layout_library import LayoutLibrary
        
        # Create layout library instance
        layout_library = LayoutLibrary()
        
        # Use enhanced layout selection
        return layout_library.select_layout_for_content(analysis, content_text, title)
    
    def optimize_content_for_layout(self, content: List[str], layout_type: str) -> List[str]:
        """
        Enhanced content optimization for all layout types
        """
        if layout_type == "bullet_list":
            # Limit to 5 bullets and truncate long items
            optimized = []
            for item in content[:5]:
                if len(item) > 80:
                    item = item[:77] + "..."
                optimized.append(item)
            return optimized
        
        elif layout_type == "two_column":
            # Balance content between columns
            optimized = []
            for item in content[:8]:  # Max 4 per column
                if len(item) > 60:
                    item = item[:57] + "..."
                optimized.append(item)
            return optimized
        
        elif layout_type == "three_column":
            # Distribute across three columns
            optimized = []
            for item in content[:9]:  # Max 3 per column
                if len(item) > 40:
                    item = item[:37] + "..."
                optimized.append(item)
            return optimized
        
        elif layout_type == "timeline":
            # Optimize for timeline milestones
            optimized = []
            for item in content[:4]:  # Max 4 milestones
                if len(item) > 30:
                    item = item[:27] + "..."
                optimized.append(item)
            return optimized
        
        elif layout_type == "process_flow":
            # Optimize for process steps
            optimized = []
            for item in content[:5]:  # Max 5 steps
                if len(item) > 40:
                    item = item[:37] + "..."
                optimized.append(item)
            return optimized
        
        elif layout_type == "pyramid":
            # Optimize for hierarchy levels
            optimized = []
            for item in content[:7]:  # Pyramid structure levels
                if len(item) > 25:
                    item = item[:22] + "..."
                optimized.append(item)
            return optimized
        
        elif layout_type == "dashboard_grid":
            # Optimize for KPI cards
            optimized = []
            for item in content[:6]:  # Max 6 KPIs
                if len(item) > 20:
                    item = item[:17] + "..."
                optimized.append(item)
            return optimized
        
        elif layout_type == "quote_highlight":
            # Optimize for quote content
            if len(content) > 0 and len(content[0]) > 200:
                return [content[0][:197] + "..."]
            return content[:1]  # Single quote
        
        elif layout_type == "split_screen":
            # Optimize for balanced panels
            optimized = []
            for item in content[:10]:  # Generous limit for panels
                if len(item) > 300:
                    item = item[:297] + "..."
                optimized.append(item)
            return optimized
        
        elif layout_type == "agenda_toc":
            # Optimize for agenda items
            optimized = []
            for item in content[:5]:  # Max 5 agenda items
                if len(item) > 60:
                    item = item[:57] + "..."
                optimized.append(item)
            return optimized
        
        else:
            # Default optimization
            return content[:7]  # Reasonable default limit