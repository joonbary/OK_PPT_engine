"""
DataAnalystAgent 테스트
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.agents.data_analyst_agent import DataAnalystAgent
from app.agents.chart_selector import ChartSelector, ChartType, InsightType
from app.services.insight_ladder import Insight, InsightLevel


@pytest.mark.asyncio
async def test_data_analyst_agent_basic():
    """기본 동작 테스트"""
    agent = DataAnalystAgent()
    
    # LLM 응답 모의
    mock_llm_response = """[
      {
        "metric": "매출",
        "value": 1000,
        "unit": "억원",
        "period": "2024년",
        "comparison": {"previous": 900, "growth_rate": 11.1},
        "context": "전년 대비 증가"
      }
    ]"""

    mock_climb_response = [
        Insight(level=InsightLevel.OBSERVATION, statement="매출이 1000억원", evidence=[], confidence=1.0),
        Insight(level=InsightLevel.COMPARISON, statement="전년 대비 11% 증가", evidence=[], confidence=0.9),
        Insight(level=InsightLevel.IMPLICATION, statement="성장세 유지", evidence=[], confidence=0.8),
        Insight(level=InsightLevel.ACTION, statement="투자 확대 필요", evidence=[], confidence=0.75),
    ]
    
    with patch.object(agent.llm_client, 'generate', new=AsyncMock(return_value=mock_llm_response)):
        with patch.object(agent.insight_ladder, 'climb', new=Mock(return_value=mock_climb_response)):
            input_data = {
                'document': "2024년 매출은 1,000억원으로 전년 대비 11% 증가했습니다.",
                'outline': [],
                'pyramid': {}
            }
            
            result = await agent.process(input_data, {'job_id': 'test_001'})
            
            # 검증
            assert 'data_points' in result
            assert 'insights' in result
            assert 'visualizations' in result
            assert 'chart_specs' in result
            
            assert len(result['data_points']) >= 1
            assert len(result['insights']) >= 1


@pytest.mark.asyncio
async def test_data_extraction():
    """데이터 추출 테스트"""
    agent = DataAnalystAgent()
    
    document = """
    2024년 우리 회사의 매출은 1,000억원으로 전년 대비 11% 증가했습니다.
    시장 점유율은 15%이며, 업계 평균인 12%를 상회합니다.
    고객 만족도는 85점으로 목표인 90점에 근접하고 있습니다.
    """
    
    mock_response = """[
      {
        "metric": "매출",
        "value": 1000,
        "unit": "억원",
        "period": "2024년",
        "comparison": {"previous": 900, "growth_rate": 11},
        "context": "전년 대비 증가"
      },
      {
        "metric": "시장점유율",
        "value": 15,
        "unit": "%",
        "period": "현재",
        "comparison": {"benchmark": 12},
        "context": "업계 평균 상회"
      },
      {
        "metric": "고객만족도",
        "value": 85,
        "unit": "점",
        "period": "현재",
        "comparison": {"target": 90},
        "context": "목표 근접"
      }
    ]"""
    
    with patch.object(agent.llm_client, 'generate', new=AsyncMock(return_value=mock_response)):
        data = await agent._extract_data(document, [])
        
        assert len(data) == 3
        assert data[0]['metric'] == '매출'
        assert data[0]['value'] == 1000
        assert data[1]['unit'] == '%'


def test_chart_selector_comparison():
    """차트 선택 - 비교 테스트"""
    selector = ChartSelector()
    
    # 적은 항목 비교
    result = selector.select_chart(
        insight_type='comparison',
        data_points=4,
        has_time_dimension=False
    )
    
    assert result['chart_type'] == ChartType.BAR_CLUSTERED
    assert 'Horizontal Bar' in result['chart_name']


def test_chart_selector_trend():
    """차트 선택 - 추세 테스트"""
    selector = ChartSelector()
    
    result = selector.select_chart(
        insight_type='trend',
        data_points=10,
        has_time_dimension=True
    )
    
    assert result['chart_type'] in [ChartType.LINE, ChartType.LINE_MARKERS]


def test_chart_selector_composition():
    """차트 선택 - 구성 테스트"""
    selector = ChartSelector()
    
    # 파이 차트 조건
    result = selector.select_chart(
        insight_type='composition',
        data_points=3,
        needs_part_to_whole=True
    )
    
    assert result['chart_type'] == ChartType.PIE


@pytest.mark.asyncio
async def test_insight_generation():
    """인사이트 생성 테스트"""
    agent = DataAnalystAgent()
    
    data_points = [
        {
            'data_id': 'data_001',
            'metric': '매출',
            'value': 1000,
            'unit': '억원',
            'period': '2024년',
            'comparison': {'previous': 900, 'growth_rate': 11.1}
        }
    ]
    
    mock_climb_response = [
        Insight(level=InsightLevel.OBSERVATION, statement="매출이 1000억원", evidence=[], confidence=1.0),
        Insight(level=InsightLevel.COMPARISON, statement="전년 대비 11% 증가", evidence=[], confidence=0.9),
        Insight(level=InsightLevel.IMPLICATION, statement="성장 모멘텀 확보", evidence=[], confidence=0.8),
        Insight(level=InsightLevel.ACTION, statement="투자 확대 필요", evidence=[], confidence=0.75),
    ]

    with patch.object(agent.insight_ladder, 'climb', new=Mock(return_value=mock_climb_response)):
        insights = await agent._generate_insights(data_points)
        
        assert len(insights) == 1
        assert insights[0]['insight_id'] == 'insight_001'
        assert 'level_4_action' in insights[0]


def test_visualization_mapping():
    """시각화 매핑 테스트"""
    agent = DataAnalystAgent()
    
    insights = [
        {
            'insight_id': 'insight_001',
            'type': 'comparison',
            'level_1_observation': '매출 1000억',
            'level_4_action': '투자 확대'
        },
        {
            'insight_id': 'insight_002',
            'type': 'trend',
            'level_1_observation': '성장률 11%',
            'level_4_action': '지속 성장'
        }
    ]
    
    visualizations = agent._map_to_visualizations(insights)
    
    assert len(visualizations) == 2
    assert visualizations[0]['viz_id'] == 'viz_001'
    assert 'chart_type' in visualizations[0]
    assert 'best_practices' in visualizations[0]


def test_chart_spec_creation():
    """차트 사양 생성 테스트"""
    agent = DataAnalystAgent()
    
    visualizations = [
        {
            'viz_id': 'viz_001',
            'insight_id': 'insight_001',
            'chart_type': 'BAR_CLUSTERED',
            'chart_name': 'Bar Chart',
            'best_practices': ['레이블 명확히', '색상 일관성']
        }
    ]
    
    specs = agent._create_chart_specs(visualizations)
    
    assert len(specs) == 1
    assert specs[0]['chart_id'] == 'chart_001'
    assert 'position' in specs[0]
    assert 'data' in specs[0]
    assert 'style' in specs[0]


def test_data_quality_validation():
    """데이터 품질 검증 테스트"""
    agent = DataAnalystAgent()
    
    data_points = [
        {
            'metric': '매출',
            'value': 1000,
            'unit': '억원'
        },
        {
            'metric': '점유율',
            'value': 'invalid',  # 잘못된 값
            'unit': '%'
        },
        {
            # 필수 필드 누락
            'metric': '만족도'
        }
    ]
    
    valid_data = agent._validate_data_quality(data_points)
    
    # 첫 번째만 유효
    assert len(valid_data) == 1
    assert valid_data[0]['metric'] == '매출'