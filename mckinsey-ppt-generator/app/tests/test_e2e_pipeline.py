
전체 파이프라인 End-to-End 테스트
실제 에이전트를 사용한 통합 테스트

"""

import pytest
from app.services.workflow_engine import WorkflowEngine
import asyncio


@pytest.mark.asyncio
@pytest.mark.integration  # 통합 테스트 마커
async def test_full_pipeline_integration():
    """
    5개 에이전트 전체 파이프라인 통합 테스트
    
    주의: 실제 LLM API를 호출하므로 시간이 오래 걸리고 비용 발생
    """
    engine = WorkflowEngine()
    
    # 실제 비즈니스 문서
    document = """
    2024년 우리 회사의 매출은 1,000억원으로 전년 대비 11% 증가했습니다.
    아시아 시장 진출을 통해 3년 내 30% 추가 성장을 목표로 합니다.
    시장 점유율은 15%로 업계 2위이며, 주요 경쟁사는 3개입니다.
    우리의 핵심 경쟁력은 AI 기술과 고객 서비스입니다.
    """
    
    input_data = {
        'job_id': 'e2e_test_001',
        'document': document,
        'num_slides': 10,  # 테스트용으로 10장
        'style': 'mckinsey',
        'target_audience': 'executive'
    }
    
    # 전체 파이프라인 실행
    result = await engine.execute(input_data)
    
    # 검증
    assert result['status'] == 'completed'
    assert result['quality_score'] >= 0.70  # 최소 품질
    assert 'ppt_data' in result
    assert len(result['ppt_data']['slides']) == 10
    
    # 슬라이드 구조 검증
    slides = result['ppt_data']['slides']
    assert slides[0]['slide_number'] == 1
    assert all('headline' in slide for slide in slides)
    assert all('colors' in slide for slide in slides)
    
    # 품질 리포트 검증
    quality_report = result['ppt_data']['quality_report']
    assert 'scores' in quality_report
    assert 'clarity' in quality_report['scores']
    
    print(f"\n=== E2E 테스트 결과 ===")
    print(f"상태: {result['status']}")
    print(f"슬라이드 수: {len(slides)}")
    print(f"품질 점수: {result['quality_score']:.3f}")
    print(f"반복 횟수: {result['iterations']}")
    print(f"처리 시간: {result['processing_time']:.2f}초")


@pytest.mark.asyncio
async def test_pipeline_stages_sequentially():
    """각 단계별 순차 테스트 (모의 데이터 사용)"""
    from unittest.mock import AsyncMock, patch
    
    engine = WorkflowEngine()
    
    # 각 에이전트의 최소 응답 정의
    minimal_responses = {
        'strategist': {
            'outline': [
                {'slide_number': 1, 'title': 'Title', 'headline': 'Main message', 'key_points': []}
            ],
            'pyramid': {'top_message': 'Core message'},
            'framework': {'framework_name': 'CUSTOM'}
        },
        'analyst': {
            'insights': [{'insight_id': '001', 'type': 'comparison'}],
            'chart_specs': [{'chart_id': '001'}],
            'data_points': []
        },
        'storyteller': {
            'scr_structure': {},
            'speaker_notes': ['Note 1'],
            'transitions': []
        },
        'designer': {
            'styled_slides': [{'slide_number': 1, 'colors': {}, 'fonts': {}}],
            'layout_selections': {},
            'design_validation': {'passed': True}
        },
        'reviewer': {
            'quality_scores': {
                'clarity': 0.9,
                'insight': 0.85,
                'structure': 0.88,
                'visual': 0.95,
                'actionability': 0.87,
                'total_score': 0.89
            },
            'passed': True,
            'improvements': []
        }
    }
    
    with patch.object(engine.strategist, 'process', new=AsyncMock(return_value=minimal_responses['strategist'])):
        with patch.object(engine.analyst, 'process', new=AsyncMock(return_value=minimal_responses['analyst'])):
            with patch.object(engine.storyteller, 'process', new=AsyncMock(return_value=minimal_responses['storyteller'])):
                with patch.object(engine.designer, 'process', new=AsyncMock(return_value=minimal_responses['designer'])):
                    with patch.object(engine.reviewer, 'process', new=AsyncMock(return_value=minimal_responses['reviewer'])):
                        with patch.object(engine, '_update_progress', new=AsyncMock()):
                            result = await engine.execute({
                                'job_id': 'stage_test',
                                'document': 'Test document',
                                'num_slides': 1
                            })
                            
                            # 모든 단계 실행 확인
                            assert engine.strategist.process.called
                            assert engine.analyst.process.called
                            assert engine.storyteller.process.called
                            assert engine.designer.process.called
                            assert engine.reviewer.process.called
                            
                            assert result['status'] == 'completed'
