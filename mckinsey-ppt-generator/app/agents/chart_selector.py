"""
McKinsey 스타일 차트 선택 로직
인사이트 유형에 따라 최적의 시각화 방법을 선택합니다.
"""

from typing import Dict, List, Optional
from enum import Enum


class ChartType(Enum):
    """python-pptx 호환 차트 타입"""
    # 비교 차트
    BAR_CLUSTERED = "BAR_CLUSTERED"
    BAR_STACKED = "BAR_STACKED"
    COLUMN_CLUSTERED = "COLUMN_CLUSTERED"
    
    # 추세 차트
    LINE = "LINE"
    LINE_MARKERS = "LINE_MARKERS"
    AREA = "AREA"
    AREA_STACKED = "AREA_STACKED"
    
    # 구성 차트
    PIE = "PIE"
    DOUGHNUT = "DOUGHNUT"
    
    # 분포 차트
    HISTOGRAM = "COLUMN_CLUSTERED"  # python-pptx에서는 COLUMN으로 표현
    
    # 관계 차트
    XY_SCATTER = "XY_SCATTER"
    BUBBLE = "BUBBLE"
    
    # 특수 차트
    WATERFALL = "WATERFALL"  # 폴백: BAR_CLUSTERED
    MATRIX_2X2 = "TABLE"      # 폴백: 테이블로 표현


class InsightType(Enum):
    """인사이트 유형"""
    COMPARISON = "comparison"      # 비교
    TREND = "trend"                # 추세
    COMPOSITION = "composition"    # 구성
    DISTRIBUTION = "distribution"  # 분포
    RELATIONSHIP = "relationship"  # 관계
    STRATEGIC = "strategic"        # 전략적 (매트릭스 등)


class ChartSelector:
    """
    McKinsey 차트 선택 알고리즘
    
    선택 기준:
    1. 인사이트 유형 (비교/추세/구성/분포/관계)
    2. 데이터 포인트 수
    3. 시간 차원 여부
    4. 데이터 복잡도
    """
    
    def __init__(self):
        self.chart_rules = self._build_chart_rules()
    
    def select_chart(
        self,
        insight_type: str,
        data_points: int,
        has_time_dimension: bool = False,
        has_multiple_series: bool = False,
        needs_part_to_whole: bool = False
    ) -> Dict:
        """
        차트 타입 선택
        
        Args:
            insight_type: 인사이트 유형 (comparison/trend/composition 등)
            data_points: 데이터 포인트 수
            has_time_dimension: 시간 차원 포함 여부
            has_multiple_series: 다중 시리즈 여부
            needs_part_to_whole: 전체 대비 부분 표현 필요 여부
        
        Returns:
            {
                'chart_type': ChartType,
                'chart_name': str,
                'reason': str,
                'best_practices': List[str]
            }
        """
        # 인사이트 타입 정규화
        insight_type_enum = self._parse_insight_type(insight_type)
        
        # 규칙 기반 선택
        if insight_type_enum == InsightType.COMPARISON:
            return self._select_comparison_chart(
                data_points, has_time_dimension, has_multiple_series
            )
        elif insight_type_enum == InsightType.TREND:
            return self._select_trend_chart(data_points, has_multiple_series)
        elif insight_type_enum == InsightType.COMPOSITION:
            return self._select_composition_chart(
                data_points, has_time_dimension, needs_part_to_whole
            )
        elif insight_type_enum == InsightType.DISTRIBUTION:
            return self._select_distribution_chart(data_points)
        elif insight_type_enum == InsightType.RELATIONSHIP:
            return self._select_relationship_chart(data_points, has_multiple_series)
        elif insight_type_enum == InsightType.STRATEGIC:
            return self._select_strategic_chart()
        else:
            # 기본값: 막대 차트
            return {
                'chart_type': ChartType.BAR_CLUSTERED,
                'chart_name': 'Horizontal Bar Chart',
                'reason': 'Default choice for general data',
                'best_practices': [
                    '레이블을 명확하게 표시',
                    '색상은 McKinsey 팔레트 사용'
                ]
            }
    
    def _select_comparison_chart(
        self,
        data_points: int,
        has_time: bool,
        has_multiple_series: bool
    ) -> Dict:
        """비교 차트 선택"""
        
        if has_time:
            # 시간 차원이 있으면 라인 차트
            return {
                'chart_type': ChartType.LINE_MARKERS,
                'chart_name': 'Line Chart with Markers',
                'reason': '시간에 따른 비교를 명확하게 표현',
                'best_practices': [
                    '마커로 데이터 포인트 강조',
                    '최대 5개 시리즈까지',
                    '범례는 차트 하단에 배치'
                ]
            }
        
        if data_points <= 5:
            # 적은 항목: 가로 막대
            chart_type = ChartType.BAR_STACKED if has_multiple_series else ChartType.BAR_CLUSTERED
            return {
                'chart_type': chart_type,
                'chart_name': 'Horizontal Bar Chart',
                'reason': f'{data_points}개 항목 비교에 최적',
                'best_practices': [
                    '값이 큰 순서대로 정렬',
                    '레이블을 왼쪽에 명확히 표시',
                    '데이터 레이블 추가'
                ]
            }
        elif data_points <= 12:
            # 중간 항목: 세로 막대
            chart_type = ChartType.COLUMN_CLUSTERED
            return {
                'chart_type': chart_type,
                'chart_name': 'Vertical Column Chart',
                'reason': f'{data_points}개 항목을 공간 효율적으로 표현',
                'best_practices': [
                    'X축 레이블 가독성 확보',
                    '그리드라인 사용',
                    '주요 항목 색상 강조'
                ]
            }
        else:
            # 많은 항목: 라인 또는 집약
            return {
                'chart_type': ChartType.LINE,
                'chart_name': 'Line Chart',
                'reason': f'{data_points}개 이상 항목은 라인이 효과적',
                'best_practices': [
                    '트렌드에 집중',
                    '주요 포인트만 마커 표시',
                    '평균선 추가 고려'
                ]
            }
    
    def _select_trend_chart(self, data_points: int, has_multiple_series: bool) -> Dict:
        """추세 차트 선택"""
        
        if has_multiple_series:
            return {
                'chart_type': ChartType.LINE_MARKERS,
                'chart_name': 'Multi-series Line Chart',
                'reason': '여러 시리즈의 추세 비교',
                'best_practices': [
                    '시리즈당 고유 색상',
                    '최대 4개 시리즈 권장',
                    '교차점 강조'
                ]
            }
        else:
            return {
                'chart_type': ChartType.LINE_MARKERS,
                'chart_name': 'Line Chart with Markers',
                'reason': '시간에 따른 변화 추적',
                'best_practices': [
                    '추세선 추가 고려',
                    '주요 변곡점 주석',
                    'Y축 0부터 시작 여부 고려'
                ]
            }
    
    def _select_composition_chart(
        self,
        data_points: int,
        has_time: bool,
        needs_part_to_whole: bool
    ) -> Dict:
        """구성 차트 선택"""
        
        if has_time:
            # 시간에 따른 구성 변화
            return {
                'chart_type': ChartType.AREA_STACKED,
                'chart_name': 'Stacked Area Chart',
                'reason': '시간에 따른 구성 변화 표현',
                'best_practices': [
                    '100% 스택 고려',
                    '중요한 카테고리를 하단에',
                    '색상 구분 명확히'
                ]
            }
        
        if data_points <= 4 and needs_part_to_whole:
            # 적은 카테고리: 파이 차트
            return {
                'chart_type': ChartType.PIE,
                'chart_name': 'Pie Chart',
                'reason': f'{data_points}개 카테고리의 비율 표현',
                'best_practices': [
                    '가장 큰 조각을 12시 방향에',
                    '퍼센트 레이블 표시',
                    '4개 이하로 제한'
                ]
            }
        else:
            # 많은 카테고리: 스택 바
            return {
                'chart_type': ChartType.BAR_STACKED,
                'chart_name': '100% Stacked Bar Chart',
                'reason': '여러 카테고리의 구성 비교',
                'best_practices': [
                    '100% 스택으로 정규화',
                    '중요 카테고리 색상 강조',
                    '총합 표시'
                ]
            }
    
    def _select_distribution_chart(self, data_points: int) -> Dict:
        """분포 차트 선택"""
        return {
            'chart_type': ChartType.HISTOGRAM,
            'chart_name': 'Histogram',
            'reason': '데이터 분포 패턴 표현',
            'best_practices': [
                '적절한 구간(bin) 수 선택',
                '평균/중앙값 표시',
                '정규 분포 곡선 추가 고려'
            ]
        }
    
    def _select_relationship_chart(self, data_points: int, has_multiple: bool) -> Dict:
        """관계 차트 선택"""
        
        if has_multiple:
            return {
                'chart_type': ChartType.BUBBLE,
                'chart_name': 'Bubble Chart',
                'reason': '3차원 관계 표현 (X, Y, 크기)',
                'best_practices': [
                    '버블 크기 범위 제한',
                    '투명도 조정',
                    '주요 버블 레이블 표시'
                ]
            }
        else:
            return {
                'chart_type': ChartType.XY_SCATTER,
                'chart_name': 'Scatter Plot',
                'reason': '두 변수 간 상관관계 표현',
                'best_practices': [
                    '추세선 추가',
                    '이상치 강조',
                    '사분면 구분선 고려'
                ]
            }
    
    def _select_strategic_chart(self) -> Dict:
        """전략 차트 (2x2 매트릭스 등)"""
        return {
            'chart_type': ChartType.MATRIX_2X2,
            'chart_name': '2x2 Matrix',
            'reason': '전략적 포지셔닝 표현',
            'best_practices': [
                '사분면별 명확한 레이블',
                '축 제목 명확히',
                '포지션별 색상 구분'
            ]
        }
    
    def _parse_insight_type(self, insight_type: str) -> InsightType:
        """문자열을 InsightType enum으로 변환"""
        type_map = {
            'comparison': InsightType.COMPARISON,
            'compare': InsightType.COMPARISON,
            'trend': InsightType.TREND,
            'time': InsightType.TREND,
            'composition': InsightType.COMPOSITION,
            'part_to_whole': InsightType.COMPOSITION,
            'distribution': InsightType.DISTRIBUTION,
            'histogram': InsightType.DISTRIBUTION,
            'relationship': InsightType.RELATIONSHIP,
            'correlation': InsightType.RELATIONSHIP,
            'strategic': InsightType.STRATEGIC,
            'matrix': InsightType.STRATEGIC
        }
        
        return type_map.get(insight_type.lower(), InsightType.COMPARISON)
    
    def _build_chart_rules(self) -> Dict:
        """차트 선택 규칙 라이브러리"""
        return {
            'comparison': {
                'description': '항목 간 크기/성과 비교',
                'charts': ['bar', 'column', 'line'],
                'avoid': ['pie', 'scatter']
            },
            'trend': {
                'description': '시간에 따른 변화',
                'charts': ['line', 'area'],
                'avoid': ['bar', 'pie']
            },
            'composition': {
                'description': '전체 대비 부분',
                'charts': ['pie', 'stacked_bar', 'treemap'],
                'avoid': ['line', 'scatter']
            },
            'distribution': {
                'description': '데이터 분포 패턴',
                'charts': ['histogram', 'box_plot'],
                'avoid': ['pie', 'line']
            },
            'relationship': {
                'description': '변수 간 상관관계',
                'charts': ['scatter', 'bubble'],
                'avoid': ['pie', 'bar']
            }
        }
