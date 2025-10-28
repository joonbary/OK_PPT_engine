"""
WorkflowEngine 단위 테스트
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.workflow_engine import WorkflowEngine
from datetime import datetime


@pytest.mark.asyncio
async def test_workflow_engine_initialization():
    """워크플로우 엔진 초기화 테스트"""
    engine = WorkflowEngine()
    
    assert engine.strategist is not None
    assert engine.analyst is not None
    assert engine.storyteller is not None
    assert engine.designer is not None
    assert engine.reviewer is not None
    assert len(engine.stages) == 6


@pytest.mark.asyncio
async def test_execute_pipeline_success():
    """전체 파이프라인 실행 성공 테스트"""
    engine = WorkflowEngine()
    
    # Mock 에이전트 응답
    mock_strategy = {
        'outline': [{'slide_number': 1, 'title': 'Test'}],
        'pyramid': {'top_message': 'Test message'},
        'framework': {'framework_name': '3C'}
    }
    
    mock_data = {
        'insights': [{'insight_id': '001'}],
        'chart_specs': [{'chart_id': '001'}]
    }
    
    mock_story = {
        'scr_structure': {},
        'speaker_notes': ['Note 1']
    }
    
    mock_design = {
        'styled_slides': [{'slide_number': 1}]
    }
    
    mock_quality = {
        'quality_scores': {'total_score': 0.90},
        'passed': True,
        'improvements': []
    }
    
    with patch.object(engine.strategist, 'process', new=AsyncMock(return_value=mock_strategy)):
        with patch.object(engine.analyst, 'process', new=AsyncMock(return_value=mock_data)):
            with patch.object(engine.storyteller, 'process', new=AsyncMock(return_value=mock_story)):
                with patch.object(engine.designer, 'process', new=AsyncMock(return_value=mock_design)):
                    with patch.object(engine.reviewer, 'process', new=AsyncMock(return_value=mock_quality)):
                        with patch.object(engine, '_update_progress', new=AsyncMock()):
                            input_data = {
                                'job_id': 'test_001',
                                'document': 'Test document',
                                'num_slides': 15
                            }
                            
                            result = await engine.execute(input_data)
                            
                            assert result['status'] == 'completed'
                            assert result['quality_score'] == 0.90
                            assert result['iterations'] == 0  # 첫 시도에 통과
                            assert 'ppt_data' in result


@pytest.mark.asyncio
async def test_execute_pipeline_with_iteration():
    """품질 미달 시 반복 개선 테스트"""
    engine = WorkflowEngine()
    
    # 첫 시도: 낮은 품질 점수
    mock_quality_low = {
        'quality_scores': {'total_score': 0.70},
        'passed': False,
        'improvements': [{'category': 'clarity', 'priority': 'high'}]
    }
    
    # 두 번째 시도: 높은 품질 점수
    mock_quality_high = {
        'quality_scores': {'total_score': 0.88},
        'passed': True,
        'improvements': []
    }
    
    mock_strategy = {
        'outline': [{'slide_number': 1}],
        'pyramid': {'top_message': 'Test'},
        'framework': {'framework_name': '3C'}
    }
    
    mock_data = {
        'insights': [{'insight_id': '001'}],
        'chart_specs': []
    }
    
    mock_story = {'scr_structure': {}, 'speaker_notes': []}
    mock_design = {'styled_slides': [{'slide_number': 1}]}
    
    with patch.object(engine.strategist, 'process', new=AsyncMock(return_value=mock_strategy)):
        with patch.object(engine.analyst, 'process', new=AsyncMock(return_value=mock_data)):
            with patch.object(engine.storyteller, 'process', new=AsyncMock(return_value=mock_story)):
                with patch.object(engine.designer, 'process', new=AsyncMock(return_value=mock_design)):
                    # 첫 시도는 낮은 점수, 두 번째는 높은 점수
                    with patch.object(engine.reviewer, 'process', new=AsyncMock(side_effect=[mock_quality_low, mock_quality_high])):
                        with patch.object(engine, '_update_progress', new=AsyncMock()):
                            input_data = {
                                'job_id': 'test_002',
                                'document': 'Test document',
                                'num_slides': 15
                            }
                            
                            result = await engine.execute(input_data)
                            
                            assert result['status'] == 'completed'
                            assert result['quality_score'] == 0.88
                            assert result['iterations'] == 1  # 1번 개선


@pytest.mark.asyncio
async def test_compile_ppt_data():
    """PPT 데이터 컴파일 테스트"""
    engine = WorkflowEngine()
    
    result = {
        'design_application': {
            'styled_slides': [
                {'slide_number': 1, 'title': 'Slide 1'},
                {'slide_number': 2, 'title': 'Slide 2'}
            ]
        },
        'quality_review': {
            'quality_scores': {'total_score': 0.90},
            'so_what_results': [],
            'improvements': []
        },
        'story_construction': {
            'speaker_notes': ['Note 1', 'Note 2']
        },
        'document_analysis': {
            'framework': {'framework_name': '3C'}
        }
    }
    
    ppt_data = engine._compile_ppt_data(result)
    
    assert 'slides' in ppt_data
    assert 'metadata' in ppt_data
    assert 'quality_report' in ppt_data
    assert len(ppt_data['slides']) == 2
    assert ppt_data['slides'][0]['speaker_notes'] == 'Note 1'
    assert ppt_data['metadata']['total_slides'] == 2


@pytest.mark.asyncio
async def test_update_progress():
    """진행 상황 업데이트 테스트"""
    engine = WorkflowEngine()
    
    mock_redis = AsyncMock()
    
    with patch('app.services.workflow_engine.get_redis', new=AsyncMock(return_value=mock_redis)):
        await engine._update_progress('test_job', 'data_extraction', 50)
        
        # Redis setex 호출 확인
        mock_redis.setex.assert_called_once()
        call_args = mock_redis.setex.call_args
        assert 'job:test_job:progress' in call_args[0]


@pytest.mark.asyncio
async def test_get_progress():
    """진행 상황 조회 테스트"""
    engine = WorkflowEngine()
    
    mock_redis = AsyncMock()
    mock_redis.get = AsyncMock(return_value='{"stage": "data_extraction", "progress": 50, "timestamp": "2024-01-01T00:00:00"}')
    
    with patch('app.services.workflow_engine.get_redis', new=AsyncMock(return_value=mock_redis)):
        progress = await engine.get_progress('test_job')
        
        assert progress['job_id'] == 'test_job'
        assert progress['stage'] == 'data_extraction'
        assert progress['progress'] == 50
