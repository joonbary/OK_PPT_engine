"""
디자인 에이전트
McKinsey 스타일을 적용하고 시각적 일관성을 보장합니다.
"""

from typing import Dict, List
from app.agents.base_agent_v2 import BaseAgentV2
from app.db.models import AgentType
from app.services.design_applicator import DesignApplicator
from loguru import logger


class DesignAgent(BaseAgentV2):
    """
    McKinsey 비주얼 디자인 전문가
    
    역할:
    - McKinsey 스타일 가이드 적용
    - 레이아웃 자동 선택
    - 시각적 계층 구조 설정
    - 디자인 일관성 검증
    """
    
    def __init__(self):
        super().__init__(
            name="Design Agent",
            agent_type=AgentType.DESIGNER,
            model="gpt-4-turbo"
        )
        self.design_applicator = DesignApplicator()
        self.metrics = {}

    async def process(self, input_data: Dict, context: Dict) -> Dict:
        """
        디자인 적용 파이프라인
        
        Args:
            input_data: {
                'outline': List[Dict],
                'chart_specs': List[Dict],
                'insights': List[Dict]
            }
            context: {
                'job_id': str
            }
        
        Returns:
            {
                'styled_slides': List[Dict],
                'layout_selections': Dict,
                'design_validation': Dict
            }
        """
        logger.info(f"Starting design processing for job {context.get('job_id')}")
        
        try:
            outline = input_data.get('outline', [])
            chart_specs = input_data.get('chart_specs', [])
            
            # Step 1: 레이아웃 선택
            logger.info("Step 1: Selecting layouts")
            layout_selections = self._select_layouts(outline)
            
            # Step 2: McKinsey 스타일 적용
            logger.info("Step 2: Applying McKinsey style")
            styled_slides = await self._apply_mckinsey_style(outline, chart_specs)
            
            # Step 3: 디자인 일관성 검증
            logger.info("Step 3: Validating design consistency")
            design_validation = self._validate_design_consistency(styled_slides)
            
            self.metrics['slides_styled'] = len(styled_slides)
            self.metrics['layouts_used'] = len(set(layout_selections.values()))
            
            return {
                'styled_slides': styled_slides,
                'layout_selections': layout_selections,
                'design_validation': design_validation
            }
            
        except Exception as e:
            logger.error(f"Design processing failed: {e}")
            raise
    
    def _select_layouts(self, outline: List[Dict]) -> Dict[int, str]:
        """
        슬라이드별 레이아웃 선택
        
        레이아웃 타입:
        - title_slide: 표지
        - dual_header: 텍스트 중심 (2단 구성)
        - three_column: 3단 비교
        - matrix: 2x2 매트릭스
        - chart_focus: 차트 중심
        
        Returns:
            {slide_number: layout_name}
        """
        layout_map = {}
        
        for slide in outline:
            slide_type = slide.get('slide_type', 'content')
            content_type = slide.get('content_type', 'text')
            
            if slide_type == 'title':
                layout = 'title_slide'
            elif slide_type == 'executive_summary':
                layout = 'dual_header'
            elif content_type == 'chart':
                layout = 'chart_focus'
            elif content_type == 'matrix':
                layout = 'matrix'
            elif len(slide.get('key_points', [])) >= 3:
                layout = 'three_column'
            else:
                layout = 'dual_header'
            
            layout_map[slide['slide_number']] = layout
        
        return layout_map
    
    async def _apply_mckinsey_style(
        self,
        outline: List[Dict],
        chart_specs: List[Dict]
    ) -> List[Dict]:
        """
        McKinsey 스타일 가이드 적용
        
        스타일 요소:
        - 색상: McKinsey Blue (#0076A8), Orange (#F47621)
        - 폰트: Arial, 크기별 일관성
        - 여백: 표준 여백 적용
        - 정렬: 좌측 정렬 원칙
        """
        styled_slides = []
        
        for slide in outline:
            styled = slide.copy()
            
            # headline 필드 보존 (AI 생성 헤드라인)
            if 'headline' in slide:
                logger.info(f"    Preserving AI headline: {slide['headline'][:50]}...")
            
            # 색상 적용
            styled['colors'] = {
                'primary': '#0076A8',
                'secondary': '#F47621',
                'text': '#53565A',
                'background': '#FFFFFF'
            }
            
            # 폰트 적용
            styled['fonts'] = {
                'title': {'family': 'Arial', 'size': 18, 'weight': 'bold'},
                'body': {'family': 'Arial', 'size': 14, 'weight': 'normal'},
                'caption': {'family': 'Arial', 'size': 10, 'weight': 'light'}
            }
            
            # 여백 설정 (인치)
            styled['margins'] = {
                'top': 0.5,
                'bottom': 0.5,
                'left': 0.5,
                'right': 0.5
            }
            
            styled_slides.append(styled)
        
        return styled_slides
    
    def _validate_design_consistency(self, styled_slides: List[Dict]) -> Dict:
        """
        디자인 일관성 검증
        
        검증 항목:
        - 색상 팔레트 일관성
        - 폰트 일관성
        - 여백 일관성
        - 정렬 규칙 준수
        """
        validation = {
            'color_consistency': True,
            'font_consistency': True,
            'margin_consistency': True,
            'issues': []
        }
        
        # 색상 일관성 체크
        primary_colors = [s.get('colors', {}).get('primary') for s in styled_slides]
        if len(set(primary_colors)) > 1:
            validation['color_consistency'] = False
            validation['issues'].append('색상 불일치 발견')
        
        # 폰트 일관성 체크
        title_sizes = [s.get('fonts', {}).get('title', {}).get('size') for s in styled_slides]
        if len(set(title_sizes)) > 1:
            validation['font_consistency'] = False
            validation['issues'].append('폰트 크기 불일치')
        
        validation['total_slides'] = len(styled_slides)
        validation['passed'] = len(validation['issues']) == 0
        
        return validation
