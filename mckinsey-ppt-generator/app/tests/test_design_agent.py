"""DesignAgent 테스트"""

import pytest
from app.agents.design_agent import DesignAgent


@pytest.mark.asyncio
async def test_design_agent_basic():
    """기본 동작 테스트"""
    agent = DesignAgent()
    
    outline = [
        {'slide_number': 1, 'slide_type': 'title', 'content_type': 'text', 'key_points': []},
        {'slide_number': 2, 'slide_type': 'content', 'content_type': 'chart', 'key_points': ['A', 'B']}
    ]
    
    result = await agent.process(
        input_data={'outline': outline, 'chart_specs': [], 'insights': []},
        context={'job_id': 'test'}
    )
    
    assert 'styled_slides' in result
    assert 'layout_selections' in result
    assert 'design_validation' in result
    assert len(result['styled_slides']) == 2


def test_layout_selection():
    """레이아웃 선택 테스트"""
    agent = DesignAgent()
    
    outline = [
        {'slide_number': 1, 'slide_type': 'title', 'content_type': 'text', 'key_points': []},
        {'slide_number': 2, 'slide_type': 'executive_summary', 'content_type': 'text', 'key_points': []},
        {'slide_number': 3, 'slide_type': 'content', 'content_type': 'chart', 'key_points': []}
    ]
    
    layouts = agent._select_layouts(outline)
    
    assert layouts[1] == 'title_slide'
    assert layouts[2] == 'dual_header'
    assert layouts[3] == 'chart_focus'


@pytest.mark.asyncio
async def test_mckinsey_style():
    """McKinsey 스타일 적용 테스트"""
    agent = DesignAgent()
    
    outline = [{'slide_number': 1, 'title': '테스트'}]
    
    styled = await agent._apply_mckinsey_style(outline, [])
    
    assert len(styled) == 1
    assert styled[0]['colors']['primary'] == '#0076A8'
    assert styled[0]['fonts']['title']['family'] == 'Arial'
