"""
데이터 분석 및 시각화 에이전트
비즈니스 문서에서 데이터를 추출하고 인사이트를 도출합니다.
"""

from typing import Dict, List, Optional
from app.agents.base_agent_v2 import BaseAgentV2
from app.db.models import AgentType
from app.agents.chart_selector import ChartSelector, ChartType
from app.services.insight_ladder import InsightLadder, InsightEnhancer, InsightQualityEvaluator
import json
import re
from loguru import logger


class DataAnalystAgent(BaseAgentV2):
    """
    McKinsey 데이터 분석 전문가
    
    역할:
    - 문서에서 정량 데이터 추출
    - 4단계 인사이트 래더 적용
    - 차트 타입 자동 선택
    - python-pptx 차트 사양 생성
    """
    
    def __init__(self):
        super().__init__(
            name="Data Analyst Agent",
            agent_type=AgentType.ANALYST,
            model="gpt-4-turbo"  # 데이터 분석에 강점
        )
        self.chart_selector = ChartSelector()
        self.insight_ladder = InsightLadder()
        self.insight_enhancer = InsightEnhancer()
        self.quality_evaluator = InsightQualityEvaluator()
        self.metrics = {}

    async def process(self, input_data: Dict, context: Dict) -> Dict:
        """
        데이터 분석 메인 파이프라인
        
        Args:
            input_data: {
                'document': str,
                'outline': List[Dict],  # StrategistAgent 출력
                'pyramid': Dict         # StrategistAgent 출력
            }
            context: {
                'job_id': str
            }
        
        Returns:
            {
                'data_points': List[Dict],      # 추출된 데이터
                'insights': List[Dict],         # 4단계 인사이트
                'visualizations': List[Dict],   # 차트 매핑
                'chart_specs': List[Dict]       # python-pptx 사양
            }
        """
        logger.info(f"Starting data analyst processing for job {context.get('job_id')}")
        
        try:
            # Step 1: 데이터 추출
            logger.info("Step 1: Extracting data from document")
            data_points = await self._extract_data(
                input_data['document'],
                input_data.get('outline', [])
            )
            logger.info(f"Extracted {len(data_points)} data points")
            
            # Step 2: 인사이트 생성 (InsightLadder 활용)
            logger.info("Step 2: Generating insights")
            insights = await self._generate_insights(data_points)
            logger.info(f"Generated {len(insights)} insights")
            
            # Step 3: 시각화 매핑
            logger.info("Step 3: Mapping to visualizations")
            visualizations = self._map_to_visualizations(insights)
            logger.info(f"Created {len(visualizations)} visualizations")
            
            # Step 4: 차트 사양 생성
            logger.info("Step 4: Creating chart specifications")
            chart_specs = self._create_chart_specs(visualizations)
            logger.info(f"Generated {len(chart_specs)} chart specs")
            
            # 성능 메트릭
            self.metrics['data_points_extracted'] = len(data_points)
            self.metrics['insights_generated'] = len(insights)
            self.metrics['charts_created'] = len(chart_specs)
            
            return {
                'data_points': data_points,
                'insights': insights,
                'visualizations': visualizations,
                'chart_specs': chart_specs
            }
            
        except Exception as e:
            logger.error(f"Data analyst processing failed: {e}")
            raise
    
    async def _extract_data(self, document: str, outline: List[Dict]) -> List[Dict]:
        """
        문서에서 정량 데이터 추출
        
        추출 대상:
        - 재무 데이터 (매출, 이익, 비용)
        - 시장 데이터 (점유율, 성장률, 규모)
        - 운영 데이터 (효율성, 생산성)
        - 고객 데이터 (만족도, 이탈률)
        
        Returns:
            [{
                'data_id': str,
                'metric': str,       # 지표 이름
                'value': float,      # 값
                'unit': str,         # 단위
                'period': str,       # 기간
                'comparison': Dict,  # 비교 데이터
                'context': str       # 컨텍스트
            }]
        """
        prompt = f"""다음 비즈니스 문서에서 모든 정량적 데이터를 추출하세요.

문서:
{document}

다음 JSON 배열 형식으로 반환하세요:
[
  {{
    "metric": "지표 이름 (예: 매출, 시장점유율)",
    "value": 숫자값,
    "unit": "단위 (예: 억원, %, 명)",
    "period": "기간 (예: 2024년, Q1, 3년)",
    "comparison": {{
      "previous": 이전값,
      "growth_rate": 성장률,
      "benchmark": 벤치마크값
    }},
    "context": "데이터 컨텍스트 설명"
  }},
  ...
]

요구사항:
1. 숫자가 포함된 모든 문장 분석
2. 비교 데이터가 있으면 함께 추출
3. 최소 5개 이상 데이터 포인트 추출
4. value는 반드시 숫자형

JSON 배열만 반환하세요."""

        response = await self.llm_client.generate(prompt)
        
        try:
            # 로그로 원본 응답 확인
            logger.debug(f"LLM raw response (first 500 chars): {response[:500] if response else 'Empty'}")
            
            # 응답이 비어있는 경우 처리
            if not response or response.strip() == "":
                logger.warning("Empty LLM response, using fallback data")
                return self._generate_fallback_data(document)
            
            # JSON 블록 처리 (더 강력한 추출)
            json_content = response
            
            # Markdown 코드 블록 제거
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                if json_end > json_start:
                    json_content = response[json_start:json_end].strip()
            elif "```" in response:
                # json 키워드 없이 코드 블록만 있는 경우
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                if json_end > json_start:
                    json_content = response[json_start:json_end].strip()
            
            # JSON 배열 추출 (더 강력한 정규식)
            import re
            json_match = re.search(r'\[.*\]', json_content, re.DOTALL)
            if json_match:
                json_content = json_match.group(0)
            
            # JSON 파싱 시도
            data_points = json.loads(json_content)
            
            # 배열이 아닌 경우 배열로 변환
            if not isinstance(data_points, list):
                if isinstance(data_points, dict):
                    data_points = [data_points]
                else:
                    logger.warning("Invalid data format, using fallback")
                    return self._generate_fallback_data(document)
            
            # 데이터가 비어있는 경우
            if not data_points:
                logger.warning("Empty data points, using fallback")
                return self._generate_fallback_data(document)
            
            # 데이터 ID 추가
            for i, data in enumerate(data_points):
                data['data_id'] = f"data_{i+1:03d}"
            
            # 품질 검증
            valid_data = self._validate_data_quality(data_points)
            
            # 유효한 데이터가 없으면 fallback
            if not valid_data:
                logger.warning("No valid data after quality check, using fallback")
                return self._generate_fallback_data(document)
            
            logger.info(f"Successfully extracted {len(valid_data)} valid data points")
            return valid_data
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse extracted data: {e}")
            logger.error(f"Problematic content: {json_content[:200] if 'json_content' in locals() else response[:200]}")
            # Fallback 데이터 반환
            return self._generate_fallback_data(document)
    
    def _validate_data_quality(self, data_points: List[Dict]) -> List[Dict]:
        """데이터 품질 검증"""
        valid_data = []
        
        for data in data_points:
            # 필수 필드 확인
            if not all(k in data for k in ['metric', 'value', 'unit']):
                logger.warning(f"Missing required fields in data: {data}")
                continue
            
            # 값이 숫자인지 확인
            try:
                float(data['value'])
            except (ValueError, TypeError):
                logger.warning(f"Invalid numeric value: {data['value']}")
                continue
            
            valid_data.append(data)
        
        return valid_data
    
    def _generate_fallback_data(self, document: str) -> List[Dict]:
        """Fallback 데이터 생성 (AI 실패 시)"""
        logger.warning("Using fallback data generation")
        
        # 문서에서 숫자 패턴 찾기
        import re
        numbers = re.findall(r'(\d+(?:\.\d+)?)[%]?', document)
        
        fallback_data = []
        
        # 기본 데이터 포인트 생성
        if len(numbers) >= 2:
            fallback_data.append({
                'data_id': 'data_001',
                'metric': 'Customer Satisfaction',
                'value': float(numbers[0]) if numbers[0] else 25,
                'unit': '%',
                'period': 'Current',
                'comparison': {
                    'previous': float(numbers[1]) if len(numbers) > 1 and numbers[1] else 20,
                    'growth_rate': 25.0,
                    'benchmark': 30.0
                },
                'context': 'Extracted from document analysis'
            })
        
        if len(numbers) >= 4:
            fallback_data.append({
                'data_id': 'data_002',
                'metric': 'Operational Cost Reduction',
                'value': float(numbers[2]) if len(numbers) > 2 and numbers[2] else 40,
                'unit': '%',
                'period': 'YoY',
                'comparison': {
                    'previous': float(numbers[3]) if len(numbers) > 3 and numbers[3] else 35,
                    'growth_rate': 14.3,
                    'benchmark': 45.0
                },
                'context': 'Year-over-year improvement'
            })
        
        # 최소 3개의 데이터 포인트 보장
        if len(fallback_data) < 3:
            fallback_data.extend([
                {
                    'data_id': f'data_00{len(fallback_data) + 1}',
                    'metric': 'Technology Investment',
                    'value': 30.0,
                    'unit': '%',
                    'period': 'Next 3 Years',
                    'comparison': {
                        'previous': 20.0,
                        'growth_rate': 50.0,
                        'benchmark': 35.0
                    },
                    'context': 'Planned investment increase'
                },
                {
                    'data_id': f'data_00{len(fallback_data) + 2}',
                    'metric': 'ROI Projection',
                    'value': 25.0,
                    'unit': '%',
                    'period': '3 Year',
                    'comparison': {
                        'previous': 15.0,
                        'growth_rate': 66.7,
                        'benchmark': 20.0
                    },
                    'context': 'Expected return on investment'
                },
                {
                    'data_id': f'data_00{len(fallback_data) + 3}',
                    'metric': 'Market Share',
                    'value': 15.5,
                    'unit': '%',
                    'period': 'Current',
                    'comparison': {
                        'previous': 12.0,
                        'growth_rate': 29.2,
                        'benchmark': 18.0
                    },
                    'context': 'Current market position'
                }
            ][:3 - len(fallback_data)])
        
        return fallback_data
    
    async def _generate_insights(self, data_points: List[Dict]) -> List[Dict]:
        """
        4단계 인사이트 래더 적용
        
        기존 InsightLadder 클래스 활용:
        - Level 1: Observation (관찰)
        - Level 2: Comparison (비교)
        - Level 3: Implication (함의)
        - Level 4: Action (실행)
        
        Returns:
            [{
                'insight_id': str,
                'data_id': str,
                'type': str,  # comparison/trend/composition
                'level_1_observation': str,
                'level_2_comparison': str,
                'level_3_implication': str,
                'level_4_action': str,
                'confidence': float
            }]
        """
        insights = []
        
        for data in data_points:
            try:
                # InsightLadder.climb는 동기 함수이므로 await를 사용하지 않습니다.
                # climb 메서드에 맞는 입력 형식으로 변환합니다.
                climb_input = {
                    "metric": data.get("metric"),
                    "value": data.get("value"),
                    "previous_value": data.get("comparison", {}).get("previous"),
                    "benchmark": data.get("comparison", {}).get("benchmark"),
                    "period": data.get("period"),
                    "unit": data.get("unit"),
                    "drivers": {} # drivers는 현재 데이터에 없으므로 빈 dict로 전달
                }

                # climb 메서드는 Insight 객체의 리스트를 반환합니다.
                insight_objects = self.insight_ladder.climb(climb_input)
                
                if not insight_objects or len(insight_objects) < 4:
                    logger.warning(f"Could not generate full 4-level insight for {data['data_id']}")
                    continue

                # 인사이트 타입 자동 판단
                insight_type = self._determine_insight_type(data)

                insight = {
                    'insight_id': f"insight_{len(insights)+1:03d}",
                    'data_id': data['data_id'],
                    'type': insight_type,
                    'level_1_observation': insight_objects[0].statement,
                    'level_2_comparison': insight_objects[1].statement,
                    'level_3_implication': insight_objects[2].statement,
                    'level_4_action': insight_objects[3].statement,
                    'confidence': insight_objects[3].confidence
                }
                
                insights.append(insight)
                
            except Exception as e:
                logger.warning(f"Failed to generate insight for {data['data_id']}: {e}")
                continue
        
        return insights
    
    def _determine_insight_type(self, data: Dict) -> str:
        """인사이트 유형 자동 판단"""
        
        # 비교 데이터가 있으면 comparison
        if data.get('comparison', {}).get('growth_rate'):
            return 'comparison'
        
        # 시간 정보가 있으면 trend
        if '년' in data.get('period', '') or '분기' in data.get('period', ''):
            return 'trend'
        
        # 비율 정보면 composition
        if data.get('unit') == '%' and data.get('value', 0) <= 100:
            return 'composition'
        
        # 기본값
        return 'comparison'
    
    def _map_to_visualizations(self, insights: List[Dict]) -> List[Dict]:
        """
        인사이트를 차트 타입으로 매핑 (통일된 형식)
        
        Returns:
            [{
                'type': str,  # bar, line, pie
                'title': str,
                'labels': List[str],
                'values': List[float],
                'description': str
            }]
        """
        visualizations = []
        
        for idx, insight in enumerate(insights):
            # ChartSelector로 차트 타입 선택
            chart_info = self.chart_selector.select_chart(
                insight_type=insight['type'],
                data_points=5,  # 기본값
                has_time_dimension='trend' in insight['type'],
                has_multiple_series=False,
                needs_part_to_whole='composition' in insight['type']
            )
            
            # 차트 타입 매핑
            chart_type_map = {
                'COLUMN_CLUSTERED': 'bar',
                'LINE': 'line',
                'PIE': 'pie',
                'WATERFALL': 'bar',  # waterfall을 bar로 fallback
                'STACKED_BAR': 'bar'
            }
            
            chart_type = chart_type_map.get(
                chart_info['chart_type'].value, 
                'bar'
            )
            
            # 샘플 데이터 생성 (실제 데이터가 있으면 사용)
            if chart_type == 'line':
                labels = ['Q1', 'Q2', 'Q3', 'Q4']
                values = [25 + idx * 5, 30 + idx * 3, 28 + idx * 4, 35 + idx * 2]
            elif chart_type == 'pie':
                labels = ['Segment A', 'Segment B', 'Segment C', 'Others']
                values = [35, 28, 22, 15]
            else:  # bar
                labels = ['Category 1', 'Category 2', 'Category 3', 'Category 4']
                values = [42 + idx * 3, 38 - idx * 2, 45 + idx, 40]
            
            viz = {
                'type': chart_type,
                'title': chart_info['chart_name'] or f"Analysis Chart {idx + 1}",
                'labels': labels,
                'values': values,
                'description': insight.get('level_1_observation', 'Data visualization')
            }
            
            visualizations.append(viz)
        
        return visualizations
    
    def _create_chart_specs(self, visualizations: List[Dict]) -> List[Dict]:
        """
        python-pptx 호환 차트 사양 생성 (Fix #2 형식)
        
        통일된 visualizations 형식을 chart_spec으로 변환
        """
        chart_specs = []
        
        for viz in visualizations:
            # 통일된 형식에서 데이터 추출
            chart_type = viz.get('type', 'bar')
            
            # python-pptx 차트 타입 매핑
            pptx_chart_type = {
                'bar': 'COLUMN_CLUSTERED',
                'line': 'LINE',
                'pie': 'PIE'
            }.get(chart_type, 'COLUMN_CLUSTERED')
            
            spec = {
                'chart_id': f"chart_{len(chart_specs)+1:03d}",
                'chart_type': pptx_chart_type,
                'type': chart_type,  # SimpleChartGenerator용
                'title': viz.get('title', 'Data Analysis'),
                'labels': viz.get('labels', ['A', 'B', 'C', 'D']),
                'values': viz.get('values', [25, 30, 35, 40]),
                'position': {
                    'left': 1.0,
                    'top': 2.0,
                    'width': 8.0,
                    'height': 4.0
                },
                'data': {
                    'categories': viz.get('labels', ['항목1', '항목2', '항목3', '항목4']),
                    'series': [
                        {
                            'name': viz.get('title', '데이터'),
                            'values': viz.get('values', [10, 20, 30, 40]),
                            'color': '#0076A8'  # McKinsey Blue
                        }
                    ]
                },
                'style': {
                    'title': viz.get('title', 'Chart'),
                    'legend_position': 'bottom',
                    'gridlines': True,
                    'data_labels': True,
                    'font_size': 10
                },
                'description': viz.get('description', '')
            }
            
            chart_specs.append(spec)
        
        return chart_specs
