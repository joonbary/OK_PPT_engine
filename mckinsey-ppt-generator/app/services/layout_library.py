"""
Layout Library for PowerPoint presentations.
Provides various layout templates optimized for different content types.
"""

from typing import Dict, List, Any, Tuple
from pptx.util import Inches, Pt
from app.core.logging import app_logger


class LayoutLibrary:
    """
    다양한 레이아웃 템플릿 라이브러리
    """
    
    def __init__(self):
        """Initialize layout library with predefined templates"""
        self.layouts = self._initialize_layouts()
        
    def _initialize_layouts(self) -> Dict[str, Dict]:
        """
        Initialize all available layouts with their configurations
        All positions are in Inches: (left, top, width, height)
        """
        return {
            # 1. Title Slide
            "title_slide": {
                "name": "Title Slide",
                "use_cases": ["프레젠테이션 시작", "섹션 구분", "Chapter 전환"],
                "elements": [
                    {
                        "type": "title",
                        "position": (Inches(0.5), Inches(2.5), Inches(9), Inches(1.5)),
                        "font_size": Pt(44),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "subtitle",
                        "position": (Inches(0.5), Inches(4), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": False,
                        "alignment": "center"
                    }
                ],
                "max_text_length": {"title": 50, "subtitle": 80}
            },
            
            # 2. Single Column (for long text)
            "single_column": {
                "name": "Single Column",
                "use_cases": ["긴 설명", "스토리텔링", "상세 분석"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "left"
                    },
                    {
                        "type": "body",
                        "position": (Inches(0.5), Inches(1.5), Inches(9), Inches(5)),
                        "font_size": Pt(11),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 7,
                        "line_spacing": 1.2
                    }
                ],
                "max_text_length": {"headline": 80, "body": 500}
            },
            
            # 3. Bullet List
            "bullet_list": {
                "name": "Bullet List",
                "use_cases": ["3-5개 핵심 포인트", "요약", "Action Items"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "left"
                    },
                    {
                        "type": "bullets",
                        "position": (Inches(0.8), Inches(1.5), Inches(8.5), Inches(4.5)),
                        "font_size": Pt(14),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 5,
                        "bullet_spacing": Pt(8),
                        "indent_level": 0.5
                    }
                ],
                "max_text_length": {"headline": 80, "bullet": 100}
            },
            
            # 4. Two Column Comparison
            "two_column": {
                "name": "Two Column Comparison",
                "use_cases": ["비교", "대조", "Before/After", "장단점 분석"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "left_column_header",
                        "position": (Inches(0.5), Inches(1.3), Inches(4.3), Inches(0.5)),
                        "font_size": Pt(16),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "left_column",
                        "position": (Inches(0.5), Inches(1.8), Inches(4.3), Inches(4.2)),
                        "font_size": Pt(11),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 4
                    },
                    {
                        "type": "right_column_header",
                        "position": (Inches(5.2), Inches(1.3), Inches(4.3), Inches(0.5)),
                        "font_size": Pt(16),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "right_column",
                        "position": (Inches(5.2), Inches(1.8), Inches(4.3), Inches(4.2)),
                        "font_size": Pt(11),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 4
                    }
                ],
                "max_text_length": {"headline": 80, "column_header": 30, "column_item": 60}
            },
            
            # 5. Three Column
            "three_column": {
                "name": "Three Column",
                "use_cases": ["3가지 옵션", "3단계 프로세스", "트리플 비교"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "col1_header",
                        "position": (Inches(0.5), Inches(1.3), Inches(2.8), Inches(0.5)),
                        "font_size": Pt(14),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "col1",
                        "position": (Inches(0.5), Inches(1.8), Inches(2.8), Inches(4.2)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 3
                    },
                    {
                        "type": "col2_header",
                        "position": (Inches(3.6), Inches(1.3), Inches(2.8), Inches(0.5)),
                        "font_size": Pt(14),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "col2",
                        "position": (Inches(3.6), Inches(1.8), Inches(2.8), Inches(4.2)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 3
                    },
                    {
                        "type": "col3_header",
                        "position": (Inches(6.7), Inches(1.3), Inches(2.8), Inches(0.5)),
                        "font_size": Pt(14),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "col3",
                        "position": (Inches(6.7), Inches(1.8), Inches(2.8), Inches(4.2)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 3
                    }
                ],
                "max_text_length": {"headline": 80, "column_header": 25, "column_item": 40}
            },
            
            # 6. Image with Text
            "image_text": {
                "name": "Image with Text",
                "use_cases": ["차트 설명", "이미지 분석", "인포그래픽"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "left"
                    },
                    {
                        "type": "image_area",
                        "position": (Inches(0.5), Inches(1.5), Inches(5), Inches(4)),
                        "placeholder": True
                    },
                    {
                        "type": "text",
                        "position": (Inches(5.8), Inches(1.5), Inches(3.7), Inches(4)),
                        "font_size": Pt(11),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 4
                    }
                ],
                "max_text_length": {"headline": 80, "text_item": 60}
            },
            
            # 7. 2x2 Matrix
            "matrix_2x2": {
                "name": "2x2 Matrix",
                "use_cases": ["SWOT 분석", "우선순위 매트릭스", "리스크 평가"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "q1_header",
                        "position": (Inches(0.5), Inches(1.3), Inches(4.3), Inches(0.3)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "q1",
                        "position": (Inches(0.5), Inches(1.6), Inches(4.3), Inches(1.9)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 3
                    },
                    {
                        "type": "q2_header",
                        "position": (Inches(5.2), Inches(1.3), Inches(4.3), Inches(0.3)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "q2",
                        "position": (Inches(5.2), Inches(1.6), Inches(4.3), Inches(1.9)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 3
                    },
                    {
                        "type": "q3_header",
                        "position": (Inches(0.5), Inches(3.8), Inches(4.3), Inches(0.3)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "q3",
                        "position": (Inches(0.5), Inches(4.1), Inches(4.3), Inches(1.9)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 3
                    },
                    {
                        "type": "q4_header",
                        "position": (Inches(5.2), Inches(3.8), Inches(4.3), Inches(0.3)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "q4",
                        "position": (Inches(5.2), Inches(4.1), Inches(4.3), Inches(1.9)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "left",
                        "max_bullets": 3
                    }
                ],
                "max_text_length": {"headline": 80, "quadrant_header": 30, "quadrant_item": 50}
            },
            
            # 8. Table Layout
            "table_layout": {
                "name": "Table Layout",
                "use_cases": ["데이터 테이블", "비교표", "스케줄"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "left"
                    },
                    {
                        "type": "table_area",
                        "position": (Inches(0.5), Inches(1.5), Inches(9), Inches(4.5)),
                        "font_size": Pt(10),
                        "table_style": "medium"
                    }
                ],
                "max_text_length": {"headline": 80, "cell": 30}
            },
            
            # 9. Timeline Layout
            "timeline": {
                "name": "Timeline Layout",
                "use_cases": ["프로젝트 일정", "역사적 순서", "단계별 진행", "마일스톤"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "timeline_line",
                        "position": (Inches(1), Inches(2), Inches(8), Inches(0.1)),
                        "line_color": "#0073E6",
                        "line_thickness": 3
                    },
                    {
                        "type": "milestone_1",
                        "position": (Inches(1.5), Inches(1.5), Inches(1.5), Inches(1)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "milestone_1_detail",
                        "position": (Inches(1.2), Inches(2.5), Inches(2.1), Inches(1.5)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center"
                    },
                    {
                        "type": "milestone_2",
                        "position": (Inches(3.5), Inches(1.5), Inches(1.5), Inches(1)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "milestone_2_detail",
                        "position": (Inches(3.2), Inches(2.5), Inches(2.1), Inches(1.5)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center"
                    },
                    {
                        "type": "milestone_3",
                        "position": (Inches(5.5), Inches(1.5), Inches(1.5), Inches(1)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "milestone_3_detail",
                        "position": (Inches(5.2), Inches(2.5), Inches(2.1), Inches(1.5)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center"
                    },
                    {
                        "type": "milestone_4",
                        "position": (Inches(7.5), Inches(1.5), Inches(1.5), Inches(1)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "milestone_4_detail",
                        "position": (Inches(7.2), Inches(2.5), Inches(2.1), Inches(1.5)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center"
                    }
                ],
                "max_text_length": {"headline": 80, "milestone": 30, "milestone_detail": 50}
            },
            
            # 10. Process Flow Layout
            "process_flow": {
                "name": "Process Flow Layout",
                "use_cases": ["프로세스 설명", "워크플로우", "단계별 가이드", "절차 설명"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "step_1",
                        "position": (Inches(0.5), Inches(1.8), Inches(2), Inches(1.5)),
                        "font_size": Pt(11),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#E8F4FD"
                    },
                    {
                        "type": "arrow_1",
                        "position": (Inches(2.7), Inches(2.3), Inches(0.6), Inches(0.5)),
                        "arrow_color": "#0073E6"
                    },
                    {
                        "type": "step_2",
                        "position": (Inches(3.5), Inches(1.8), Inches(2), Inches(1.5)),
                        "font_size": Pt(11),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#E8F4FD"
                    },
                    {
                        "type": "arrow_2",
                        "position": (Inches(5.7), Inches(2.3), Inches(0.6), Inches(0.5)),
                        "arrow_color": "#0073E6"
                    },
                    {
                        "type": "step_3",
                        "position": (Inches(6.5), Inches(1.8), Inches(2), Inches(1.5)),
                        "font_size": Pt(11),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#E8F4FD"
                    },
                    {
                        "type": "step_4",
                        "position": (Inches(2), Inches(4), Inches(2), Inches(1.5)),
                        "font_size": Pt(11),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#E8F4FD"
                    },
                    {
                        "type": "arrow_3",
                        "position": (Inches(4.2), Inches(4.3), Inches(0.6), Inches(0.5)),
                        "arrow_color": "#0073E6"
                    },
                    {
                        "type": "step_5",
                        "position": (Inches(5), Inches(4), Inches(2), Inches(1.5)),
                        "font_size": Pt(11),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#E8F4FD"
                    }
                ],
                "max_text_length": {"headline": 80, "step": 40}
            },
            
            # 11. Pyramid Hierarchy Layout
            "pyramid": {
                "name": "Pyramid Hierarchy Layout",
                "use_cases": ["조직도", "우선순위", "계층구조", "피라미드 구조"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "level_1",
                        "position": (Inches(4), Inches(1.5), Inches(2), Inches(0.8)),
                        "font_size": Pt(14),
                        "bold": True,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#0073E6",
                        "text_color": "#FFFFFF"
                    },
                    {
                        "type": "level_2_left",
                        "position": (Inches(2), Inches(2.8), Inches(2), Inches(0.7)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#4A90E2"
                    },
                    {
                        "type": "level_2_right",
                        "position": (Inches(6), Inches(2.8), Inches(2), Inches(0.7)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#4A90E2"
                    },
                    {
                        "type": "level_3_1",
                        "position": (Inches(0.5), Inches(4.1), Inches(1.8), Inches(0.6)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#A8CCE8"
                    },
                    {
                        "type": "level_3_2",
                        "position": (Inches(2.6), Inches(4.1), Inches(1.8), Inches(0.6)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#A8CCE8"
                    },
                    {
                        "type": "level_3_3",
                        "position": (Inches(4.7), Inches(4.1), Inches(1.8), Inches(0.6)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#A8CCE8"
                    },
                    {
                        "type": "level_3_4",
                        "position": (Inches(6.8), Inches(4.1), Inches(1.8), Inches(0.6)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#A8CCE8"
                    }
                ],
                "max_text_length": {"headline": 80, "level_1": 30, "level_2": 25, "level_3": 20}
            },
            
            # 12. Dashboard Grid Layout
            "dashboard_grid": {
                "name": "Dashboard Grid Layout",
                "use_cases": ["KPI 대시보드", "지표 모니터링", "성과 측정", "메트릭스 요약"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "kpi_1",
                        "position": (Inches(0.5), Inches(1.5), Inches(2.8), Inches(1.8)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rect",
                        "background_color": "#F8F9FA",
                        "border_color": "#DEE2E6"
                    },
                    {
                        "type": "kpi_2",
                        "position": (Inches(3.6), Inches(1.5), Inches(2.8), Inches(1.8)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rect",
                        "background_color": "#F8F9FA",
                        "border_color": "#DEE2E6"
                    },
                    {
                        "type": "kpi_3",
                        "position": (Inches(6.7), Inches(1.5), Inches(2.8), Inches(1.8)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rect",
                        "background_color": "#F8F9FA",
                        "border_color": "#DEE2E6"
                    },
                    {
                        "type": "kpi_4",
                        "position": (Inches(0.5), Inches(3.7), Inches(2.8), Inches(1.8)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rect",
                        "background_color": "#F8F9FA",
                        "border_color": "#DEE2E6"
                    },
                    {
                        "type": "kpi_5",
                        "position": (Inches(3.6), Inches(3.7), Inches(2.8), Inches(1.8)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rect",
                        "background_color": "#F8F9FA",
                        "border_color": "#DEE2E6"
                    },
                    {
                        "type": "kpi_6",
                        "position": (Inches(6.7), Inches(3.7), Inches(2.8), Inches(1.8)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rect",
                        "background_color": "#F8F9FA",
                        "border_color": "#DEE2E6"
                    }
                ],
                "max_text_length": {"headline": 80, "kpi_title": 20, "kpi_value": 15, "kpi_description": 30}
            },
            
            # 13. Quote Highlight Layout
            "quote_highlight": {
                "name": "Quote Highlight Layout",
                "use_cases": ["인용문", "고객 후기", "추천사", "중요 메시지"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "quote_box",
                        "position": (Inches(1), Inches(1.5), Inches(8), Inches(3)),
                        "font_size": Pt(16),
                        "bold": False,
                        "alignment": "center",
                        "shape_type": "rounded_rect",
                        "background_color": "#F0F8FF",
                        "border_color": "#0073E6",
                        "line_spacing": 1.5
                    },
                    {
                        "type": "attribution",
                        "position": (Inches(1.5), Inches(4.8), Inches(7), Inches(0.8)),
                        "font_size": Pt(12),
                        "bold": True,
                        "alignment": "right"
                    },
                    {
                        "type": "context",
                        "position": (Inches(1.5), Inches(5.3), Inches(7), Inches(0.5)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "right",
                        "italic": True
                    }
                ],
                "max_text_length": {"headline": 80, "quote": 200, "attribution": 50, "context": 80}
            },
            
            # 14. Split Screen Layout
            "split_screen": {
                "name": "Split Screen Layout",
                "use_cases": ["50/50 분할", "대등 비교", "좌우 균형", "대칭 구조"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "left_panel",
                        "position": (Inches(0.5), Inches(1.5), Inches(4.3), Inches(4.5)),
                        "font_size": Pt(12),
                        "bold": False,
                        "alignment": "left",
                        "shape_type": "rect",
                        "background_color": "#F8F9FA",
                        "border_color": "#DEE2E6"
                    },
                    {
                        "type": "right_panel",
                        "position": (Inches(5.2), Inches(1.5), Inches(4.3), Inches(4.5)),
                        "font_size": Pt(12),
                        "bold": False,
                        "alignment": "left",
                        "shape_type": "rect",
                        "background_color": "#F8F9FA",
                        "border_color": "#DEE2E6"
                    },
                    {
                        "type": "divider_line",
                        "position": (Inches(4.8), Inches(1.5), Inches(0.1), Inches(4.5)),
                        "line_color": "#DEE2E6",
                        "line_thickness": 2
                    }
                ],
                "max_text_length": {"headline": 80, "panel": 300}
            },
            
            # 15. Agenda/TOC Layout
            "agenda_toc": {
                "name": "Agenda/TOC Layout",
                "use_cases": ["의제", "목차", "일정표", "순서 안내"],
                "elements": [
                    {
                        "type": "headline",
                        "position": (Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)),
                        "font_size": Pt(24),
                        "bold": True,
                        "alignment": "center"
                    },
                    {
                        "type": "agenda_item_1",
                        "position": (Inches(1), Inches(1.5), Inches(8), Inches(0.6)),
                        "font_size": Pt(14),
                        "bold": True,
                        "alignment": "left",
                        "number_prefix": "1."
                    },
                    {
                        "type": "agenda_item_2",
                        "position": (Inches(1), Inches(2.3), Inches(8), Inches(0.6)),
                        "font_size": Pt(14),
                        "bold": True,
                        "alignment": "left",
                        "number_prefix": "2."
                    },
                    {
                        "type": "agenda_item_3",
                        "position": (Inches(1), Inches(3.1), Inches(8), Inches(0.6)),
                        "font_size": Pt(14),
                        "bold": True,
                        "alignment": "left",
                        "number_prefix": "3."
                    },
                    {
                        "type": "agenda_item_4",
                        "position": (Inches(1), Inches(3.9), Inches(8), Inches(0.6)),
                        "font_size": Pt(14),
                        "bold": True,
                        "alignment": "left",
                        "number_prefix": "4."
                    },
                    {
                        "type": "agenda_item_5",
                        "position": (Inches(1), Inches(4.7), Inches(8), Inches(0.6)),
                        "font_size": Pt(14),
                        "bold": True,
                        "alignment": "left",
                        "number_prefix": "5."
                    },
                    {
                        "type": "time_info",
                        "position": (Inches(7), Inches(5.5), Inches(2.5), Inches(0.5)),
                        "font_size": Pt(10),
                        "bold": False,
                        "alignment": "right",
                        "italic": True
                    }
                ],
                "max_text_length": {"headline": 80, "agenda_item": 60, "time_info": 30}
            }
        }
    
    def get_layout(self, layout_name: str) -> Dict[str, Any]:
        """
        Get specific layout configuration by name
        """
        if layout_name in self.layouts:
            return self.layouts[layout_name]
        else:
            app_logger.warning(f"Layout '{layout_name}' not found, using default")
            return self.layouts["single_column"]
    
    def select_layout_for_content(self, content_analysis: Dict[str, Any], content_text: str = "", title: str = "") -> str:
        """
        Enhanced layout selection with keyword-based hints and advanced analysis
        """
        content_type = content_analysis.get("content_type", "paragraph")
        complexity = content_analysis.get("complexity", "simple")
        has_chart = content_analysis.get("has_chart", False)
        has_table = content_analysis.get("has_table", False)
        bullet_count = content_analysis.get("bullet_count", 0)
        text_density = content_analysis.get("text_density", "medium")
        
        # Combine title and content for keyword analysis
        combined_text = (title + " " + content_text).lower()
        
        # 1. Keyword-based layout hints (highest priority)
        keyword_layout = self._detect_layout_keywords(combined_text)
        if keyword_layout:
            return keyword_layout
        
        # 2. Content type based selection with enhanced logic
        if content_type == "title_only":
            return "title_slide"
        
        elif content_type == "matrix":
            # Distinguish between different matrix types
            if "swot" in combined_text or "2x2" in combined_text:
                return "matrix_2x2"
            elif "dashboard" in combined_text or "kpi" in combined_text:
                return "dashboard_grid"
            else:
                return "matrix_2x2"
        
        elif has_table:
            # Check if it's a dashboard-style table
            if any(kw in combined_text for kw in ["dashboard", "kpi", "metrics", "지표"]):
                return "dashboard_grid"
            else:
                return "table_layout"
        
        elif content_type == "comparison":
            # Enhanced comparison detection
            if any(kw in combined_text for kw in ["vs", "versus", "split", "50/50"]):
                return "split_screen"
            elif bullet_count > 6:
                return "three_column"
            else:
                return "two_column"
        
        elif content_type == "image_text" or has_chart:
            return "image_text"
        
        elif content_type == "list":
            # Check for agenda/TOC patterns
            if self._is_agenda_pattern(combined_text, bullet_count):
                return "agenda_toc"
            elif bullet_count > 6:
                return "two_column"  # Split long lists
            else:
                return "bullet_list"
        
        elif text_density == "high":
            # Check if it needs split screen for balanced presentation
            if len(combined_text.split()) > 200:
                return "split_screen"
            else:
                return "two_column"
        
        elif complexity == "simple" and text_density == "low":
            return "title_slide"
        
        else:
            return "single_column"
    
    def _detect_layout_keywords(self, text: str) -> str:
        """
        Detect specific layout keywords to suggest optimal layout
        """
        # Timeline keywords (avoid overlap with agenda)
        timeline_keywords = [
            "timeline", "타임라인", "roadmap", "로드맵", 
            "milestone", "마일스톤", "chronology", 
            "history", "역사", "progression", "진행"
        ]
        
        # Process flow keywords
        process_keywords = [
            "process", "프로세스", "workflow", "워크플로우", "step", "단계", 
            "procedure", "절차", "method", "방법", "flow", "흐름", 
            "guide", "가이드", "instruction", "지시"
        ]
        
        # Pyramid hierarchy keywords
        pyramid_keywords = [
            "pyramid", "피라미드", "hierarchy", "계층", "organization", "조직", 
            "structure", "구조", "level", "레벨", "rank", "순위", 
            "priority", "우선순위"
        ]
        
        # Dashboard keywords
        dashboard_keywords = [
            "dashboard", "대시보드", "kpi", "metrics", "지표", "performance", "성과", 
            "monitoring", "모니터링", "scorecard", "스코어카드", "gauge", "게이지"
        ]
        
        # Quote keywords
        quote_keywords = [
            "quote", "인용", "testimonial", "추천", "review", "후기", 
            "feedback", "피드백", "opinion", "의견", "comment", "코멘트",
            "says", "said", "라고", "말한다"
        ]
        
        # Split screen keywords
        split_keywords = [
            "split", "분할", "divide", "나누기", "50/50", "half", "절반", 
            "side by side", "나란히", "parallel", "병렬", "comparison", "비교"
        ]
        
        # Agenda keywords (higher priority than timeline for overlap resolution)
        agenda_keywords = [
            "agenda", "의제", "toc", "table of contents", "목차", "outline", "개요", 
            "schedule", "일정", "program", "프로그램", "contents", "내용"
        ]
        
        # Check for each layout type with specific priority order
        # Agenda gets priority over timeline for overlapping keywords
        if any(keyword in text for keyword in agenda_keywords):
            return "agenda_toc"
        elif any(keyword in text for keyword in timeline_keywords):
            return "timeline"
        elif any(keyword in text for keyword in process_keywords):
            return "process_flow"
        elif any(keyword in text for keyword in pyramid_keywords):
            return "pyramid"
        elif any(keyword in text for keyword in dashboard_keywords):
            return "dashboard_grid"
        elif any(keyword in text for keyword in quote_keywords):
            return "quote_highlight"
        elif any(keyword in text for keyword in split_keywords):
            return "split_screen"
        
        return None
    
    def _is_agenda_pattern(self, text: str, bullet_count: int) -> bool:
        """
        Detect if content follows agenda/TOC pattern
        """
        # Check for numbered items or agenda-like structure
        agenda_indicators = [
            "1.", "2.", "3.", "4.", "5.",
            "first", "second", "third", "fourth", "fifth",
            "첫째", "둘째", "셋째", "넷째", "다섯째",
            "agenda", "의제", "schedule", "일정"
        ]
        
        # Must have reasonable number of items for agenda
        if 3 <= bullet_count <= 6:
            if any(indicator in text for indicator in agenda_indicators):
                return True
        
        return False
    
    def get_text_limits_for_layout(self, layout_name: str) -> Dict[str, int]:
        """
        Get text length limits for specific layout
        """
        layout = self.get_layout(layout_name)
        return layout.get("max_text_length", {
            "default": 100,
            "title": 50,
            "body": 500
        })
    
    def calculate_dynamic_font_size(self, text: str, base_font_size: int, 
                                   max_width_inches: float) -> int:
        """
        Calculate dynamic font size based on text length and available width
        """
        text_length = len(text)
        
        # Rough calculation: assume ~10 chars per inch at 12pt
        chars_per_inch = 10 * (12 / base_font_size)
        max_chars = max_width_inches * chars_per_inch
        
        if text_length <= max_chars:
            return base_font_size
        else:
            # Reduce font size proportionally
            reduction_factor = max_chars / text_length
            new_font_size = int(base_font_size * reduction_factor)
            # Minimum font size: 8pt
            return max(8, new_font_size)
    
    def get_layout_fallback_chain(self, primary_layout: str) -> List[str]:
        """
        Get fallback layout chain for similar layouts
        """
        fallback_chains = {
            "timeline": ["process_flow", "bullet_list", "single_column"],
            "process_flow": ["timeline", "bullet_list", "single_column"],
            "pyramid": ["matrix_2x2", "three_column", "two_column"],
            "dashboard_grid": ["matrix_2x2", "three_column", "table_layout"],
            "quote_highlight": ["single_column", "title_slide"],
            "split_screen": ["two_column", "single_column"],
            "agenda_toc": ["bullet_list", "single_column"],
            "bullet_list": ["two_column", "single_column"],
            "two_column": ["three_column", "single_column"],
            "three_column": ["two_column", "single_column"],
            "matrix_2x2": ["dashboard_grid", "three_column", "two_column"],
            "image_text": ["split_screen", "single_column"],
            "table_layout": ["dashboard_grid", "matrix_2x2", "single_column"],
            "title_slide": ["quote_highlight", "single_column"],
            "single_column": ["bullet_list", "two_column"]
        }
        
        return fallback_chains.get(primary_layout, ["single_column"])
    
    def calculate_layout_complexity_score(self, layout_name: str, content_analysis: Dict) -> float:
        """
        Calculate complexity score for layout selection (0.0 = simple, 1.0 = complex)
        """
        base_complexity = {
            "title_slide": 0.1,
            "single_column": 0.2,
            "bullet_list": 0.3,
            "quote_highlight": 0.3,
            "two_column": 0.4,
            "split_screen": 0.5,
            "image_text": 0.5,
            "agenda_toc": 0.5,
            "three_column": 0.6,
            "table_layout": 0.7,
            "timeline": 0.7,
            "process_flow": 0.8,
            "pyramid": 0.8,
            "matrix_2x2": 0.8,
            "dashboard_grid": 0.9
        }
        
        complexity_score = base_complexity.get(layout_name, 0.5)
        
        # Adjust based on content factors
        bullet_count = content_analysis.get("bullet_count", 0)
        text_density = content_analysis.get("text_density", "medium")
        
        # Increase complexity for more bullets
        if bullet_count > 5:
            complexity_score += 0.1
        elif bullet_count > 8:
            complexity_score += 0.2
        
        # Adjust for text density
        if text_density == "high":
            complexity_score += 0.1
        elif text_density == "low":
            complexity_score -= 0.1
        
        return min(1.0, max(0.0, complexity_score))
    
    def get_layout_variants(self, layout_name: str) -> Dict[str, Dict]:
        """
        Get layout variants (compact/standard/spacious)
        """
        base_layout = self.get_layout(layout_name)
        if not base_layout:
            return {}
        
        variants = {}
        
        # Standard variant (existing layout)
        variants["standard"] = base_layout
        
        # Compact variant (smaller spacing, smaller fonts)
        compact_layout = self._create_layout_variant(base_layout, "compact")
        variants["compact"] = compact_layout
        
        # Spacious variant (larger spacing, larger fonts)
        spacious_layout = self._create_layout_variant(base_layout, "spacious")
        variants["spacious"] = spacious_layout
        
        return variants
    
    def _create_layout_variant(self, base_layout: Dict, variant_type: str) -> Dict:
        """
        Create layout variant with adjusted spacing and fonts
        """
        import copy
        variant_layout = copy.deepcopy(base_layout)
        
        for element in variant_layout.get("elements", []):
            if variant_type == "compact":
                # Reduce font sizes and spacing
                if "font_size" in element:
                    current_size = element["font_size"].pt if hasattr(element["font_size"], 'pt') else element["font_size"]
                    element["font_size"] = Pt(max(8, int(current_size * 0.9)))
                
                # Reduce spacing between elements
                position = element.get("position", [])
                if len(position) >= 2:
                    # Reduce top positioning by 10%
                    new_top = position[1].inches * 0.95 if hasattr(position[1], 'inches') else position[1] * 0.95
                    element["position"] = (position[0], Inches(new_top), position[2], position[3])
            
            elif variant_type == "spacious":
                # Increase font sizes and spacing
                if "font_size" in element:
                    current_size = element["font_size"].pt if hasattr(element["font_size"], 'pt') else element["font_size"]
                    element["font_size"] = Pt(min(28, int(current_size * 1.1)))
                
                # Increase spacing between elements
                position = element.get("position", [])
                if len(position) >= 2:
                    # Increase top positioning by 10%
                    new_top = position[1].inches * 1.05 if hasattr(position[1], 'inches') else position[1] * 1.05
                    element["position"] = (position[0], Inches(new_top), position[2], position[3])
        
        return variant_layout
    
    def validate_layout_compatibility(self, layout_name: str, content_analysis: Dict) -> Dict[str, Any]:
        """
        Validate if layout is compatible with content requirements
        """
        layout = self.get_layout(layout_name)
        if not layout:
            return {"compatible": False, "issues": ["Layout not found"]}
        
        issues = []
        warnings = []
        
        # Check bullet count compatibility
        bullet_count = content_analysis.get("bullet_count", 0)
        if layout_name in ["bullet_list", "two_column", "three_column"]:
            max_bullets = self._get_max_bullets_for_layout(layout_name)
            if bullet_count > max_bullets:
                warnings.append(f"Content has {bullet_count} bullets but layout supports max {max_bullets}")
        
        # Check text density compatibility
        text_density = content_analysis.get("text_density", "medium")
        if text_density == "high" and layout_name in ["title_slide", "quote_highlight"]:
            issues.append("High text density not suitable for this layout")
        
        # Check complexity compatibility
        complexity = content_analysis.get("complexity", "simple")
        layout_complexity = self.calculate_layout_complexity_score(layout_name, content_analysis)
        
        complexity_scores = {"simple": 0.3, "medium": 0.6, "complex": 0.9}
        content_complexity = complexity_scores.get(complexity, 0.5)
        
        if abs(layout_complexity - content_complexity) > 0.4:
            warnings.append(f"Layout complexity mismatch: content is {complexity}, layout is {layout_complexity:.1f}")
        
        return {
            "compatible": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "compatibility_score": max(0.0, 1.0 - len(issues) * 0.5 - len(warnings) * 0.1)
        }
    
    def _get_max_bullets_for_layout(self, layout_name: str) -> int:
        """
        Get maximum bullet points supported by layout
        """
        max_bullets = {
            "bullet_list": 5,
            "two_column": 8,  # 4 per column
            "three_column": 9,  # 3 per column
            "matrix_2x2": 12,  # 3 per quadrant
            "timeline": 4,
            "process_flow": 5,
            "pyramid": 7,
            "dashboard_grid": 6,
            "agenda_toc": 5
        }
        
        return max_bullets.get(layout_name, 10)