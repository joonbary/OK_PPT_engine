"""StorytellerAgent 테스트"""

import pytest
from unittest.mock import AsyncMock, patch
from app.agents.storyteller_agent import StorytellerAgent


@pytest.mark.asyncio
async def test_storyteller_basic():
    """기본 동작 테스트"""
    agent = StorytellerAgent()
    
    outline = [
        {'slide_number': 1, 'title': '표지', 'slide_type': 'title', 'headline': '핵심 메시지', 'key_points': []},
        {'slide_number': 2, 'title': '요약', 'slide_type': 'executive_summary', 'headline': '요약', 'key_points': ['포인트1']},
        {'slide_number': 3, 'title': '상황', 'slide_type': 'situation', 'headline': '현황', 'key_points': []}
    ]
    
    mock_scr = '{"situation_slides": [1,2], "complication_slides": [3], "resolution_slides": [], "story_arc": "테스트"}'
    
    with patch.object(agent.llm_client, 'generate', new=AsyncMock(side_effect=[
        mock_scr,  # SCR 구조
        "다음으로 넘어가겠습니다.",  # 전환 1
        "이제 현황을 살펴보겠습니다.",  # 전환 2
        "문제점을 분석하겠습니다."  # 전환 3
    ])):
        result = await agent.process(
            input_data={'outline': outline, 'pyramid': {}, 'insights': []},
            context={'job_id': 'test'}
        )
        
        assert 'scr_structure' in result
        assert 'transitions' in result
        assert 'speaker_notes' in result
        assert len(result['speaker_notes']) == len(outline)


@pytest.mark.asyncio
async def test_scr_structure():
    """SCR 구조 적용 테스트"""
    agent = StorytellerAgent()
    
    outline = [{'slide_number': i, 'title': f'슬라이드 {i}'} for i in range(1, 11)]
    pyramid = {'top_message': '핵심 메시지'}
    
    mock_scr = '{"situation_slides": [1,2,3], "complication_slides": [4,5], "resolution_slides": [6,7,8,9,10], "story_arc": "상황→문제→해결"}'
    
    with patch.object(agent.llm_client, 'generate', new=AsyncMock(return_value=mock_scr)):
        scr = await agent._apply_scr_structure(outline, pyramid)
        
        assert 'situation_slides' in scr
        assert 'complication_slides' in scr
        assert 'resolution_slides' in scr
        assert len(scr['situation_slides']) >= 2
