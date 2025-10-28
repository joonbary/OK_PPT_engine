"""QualityReviewAgent 테스트"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.agents.quality_review_agent import QualityReviewAgent


@pytest.mark.asyncio
async def test_quality_review_basic():
    """기본 동작 테스트"""
    agent = QualityReviewAgent()
    
    styled_slides = [
        {'slide_number': 1, 'headline': '아시아 시장 진출로 3년 내 매출 30% 성장 실현'},
        {'slide_number': 2, 'headline': '기술 우위로 경쟁력 확보'}
    ]
    
    with patch.object(agent.so_what_tester, 'test', return_value={'score': 0.9, 'issues': []}):
        with patch.object(agent.quality_controller, 'evaluate', return_value={
            'scores': {
                'clarity': 0.9,
                'insight': 0.85,
                'structure': 0.8,
                'visual': 0.95,
                'actionability': 0.88,
                'total_score': 0.876
            }
        }):
            result = await agent.process(
                input_data={'styled_slides': styled_slides, 'insights': [], 'pyramid': {}},
                context={'job_id': 'test'}
            )
            
            assert 'quality_scores' in result
            assert 'so_what_results' in result
            assert 'improvements' in result
            assert 'passed' in result
            assert result['passed'] == True  # 0.876 >= 0.85


@pytest.mark.asyncio
async def test_so_what_tests():
    """So What 테스트"""
    agent = QualityReviewAgent()
    
    slides = [
        {'slide_number': 1, 'headline': '좋은 헤드라인'},
        {'slide_number': 2, 'headline': '나쁜'}
    ]
    
    with patch.object(agent.so_what_tester, 'test', side_effect=[
        {'score': 0.9, 'issues': []},
        {'score': 0.3, 'issues': ['So What 불명확']}
    ]):
        results = await agent._run_so_what_tests(slides)
        
        assert len(results) == 2
        assert results[0]['passed'] == True
        assert results[1]['passed'] == False


@pytest.mark.asyncio
async def test_improvement_generation():
    """개선 제안 생성 테스트"""
    agent = QualityReviewAgent()
    
    quality_scores = {
        'clarity': 0.6,  # 낮음
        'insight': 0.9,
        'structure': 0.75,  # 낮음
        'visual': 0.95,
        'actionability': 0.88
    }
    
    so_what_results = [
        {'slide_number': 1, 'passed': False}
    ]
    
    improvements = await agent._generate_improvements(quality_scores, so_what_results)
    
    assert len(improvements) >= 2  # clarity, structure
    assert any(i['category'] == 'clarity' for i in improvements)
