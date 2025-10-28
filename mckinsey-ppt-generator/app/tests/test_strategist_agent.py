"""
StrategistAgent 테스트
"""

import pytest
import json
from app.agents.strategist_agent import StrategistAgent
from app.agents.frameworks import MECEFrameworkLibrary


@pytest.mark.asyncio
async def test_strategist_agent_basic(mocker):
    """기본 동작 테스트"""
    agent = StrategistAgent()

    # Mock LLM responses
    analysis_response = {
        "key_message": "아시아 시장 진출로 3년 내 매출 3배 성장 실현",
        "data_points": ["연매출 500억원", "병원 50곳 납품", "목표 매출 1,500억원"],
        "target_audience": "executive",
        "purpose": "의사결정",
        "context": "AI 헬스케어 솔루션의 아시아 시장 진출 전략",
        "industry": "healthcare_tech"
    }
    pyramid_response = {
        "top_message": "AI 헬스케어 솔루션의 아시아 진출로 3년 내 매출 1,500억 달성 가능",
        "supporting_arguments": [
            {"argument": "국내 검증된 기술력으로 경쟁 우위 확보", "category": "Company", "evidence": ["병원 50곳 성공 사례", "AI 정확도 95%", "특허 30개"]},
            {"argument": "현지 경쟁사 대비 기술 격차 2년 이상", "category": "Competitors", "evidence": ["글로벌 기업 아시아 진출 부진", "현지 스타트업 기술 한계"]},
            {"argument": "아시아 헬스케어 시장 연 12% 성장", "category": "Customers", "evidence": ["시장 규모 50조원", "디지털 헬스 수요 급증"]}
        ]
    }
    outline_response = []
    for i in range(15):
        outline_response.append({
            "slide_number": i + 1,
            "slide_type": "title" if i == 0 else "content",
            "title": f"슬라이드 {i+1}",
            "headline": f"헤드라인 {i+1}",
            "content_type": "text",
            "key_points": [],
            "data_requirements": [],
            "layout_suggestion": "title_slide",
            "category": "intro"
        })

    mocker.patch.object(agent.llm_client, 'generate', side_effect=[
        json.dumps(analysis_response),
        json.dumps(pyramid_response),
        json.dumps(outline_response)
    ])

    input_data = {
        'document': "우리 회사는 아시아 시장 진출을 고려하고 있습니다.",
        'num_slides': 15
    }

    result = await agent.process(input_data, {'job_id': 'test_001'})

    # 검증
    assert 'analysis' in result
    assert 'framework' in result
    assert 'pyramid' in result
    assert 'outline' in result
    assert len(result['outline']) == 15
    assert result['outline'][0]['slide_type'] == 'title'
    assert all('headline' in slide for slide in result['outline'])


@pytest.mark.asyncio
async def test_document_analysis(mocker):
    """문서 분석 테스트"""
    agent = StrategistAgent()
    analysis_response = {
        "key_message": "아시아 시장 진출로 30% 성장 가능",
        "data_points": ["매출 1,000억", "시장 점유율 15%"],
        "target_audience": "executive",
        "purpose": "의사결정",
        "context": "AI 헬스케어 솔루션의 아시아 시장 진출 전략",
        "industry": "healthcare_tech"
    }
    mocker.patch.object(agent.llm_client, 'generate', return_value=json.dumps(analysis_response))

    document = "2024년 우리 회사의 매출은 1,000억원으로 전년 대비 11% 증가했습니다."
    analysis = await agent._analyze_document(document)

    assert 'key_message' in analysis
    assert 'data_points' in analysis
    assert len(analysis['data_points']) > 0

def test_framework_selection():
    """프레임워크 선택 테스트"""
    agent = StrategistAgent()
    analysis = {
        'purpose': 'market_entry',
        'context': '아시아 시장 진출 전략 수립',
        'industry': 'technology'
    }
    framework = agent._select_framework(analysis)
    assert framework['framework_name'] == '3C'


@pytest.mark.asyncio
async def test_pyramid_structure(mocker):
    """피라미드 구조 생성 테스트"""
    agent = StrategistAgent()
    pyramid_response = {
        "top_message": "AI 헬스케어 솔루션의 아시아 진출로 3년 내 매출 1,500억 달성 가능",
        "supporting_arguments": [
            {"argument": "국내 검증된 기술력으로 경쟁 우위 확보", "category": "Company", "evidence": []},
            {"argument": "현지 경쟁사 대비 기술 격차 2년 이상", "category": "Competitors", "evidence": []},
            {"argument": "아시아 헬스케어 시장 연 12% 성장", "category": "Customers", "evidence": []}
        ]
    }
    mocker.patch.object(agent.llm_client, 'generate', return_value=json.dumps(pyramid_response))

    analysis = {'key_message': '아시아 시장 진출로 30% 성장 가능'}
    framework = {
        'framework_name': '3C',
        'categories': ['Company', 'Competitors', 'Customers'],
        'description': '3C 분석'
    }
    pyramid = await agent._create_pyramid_structure(analysis, framework)

    assert 'top_message' in pyramid
    assert len(pyramid['supporting_arguments']) == 3


@pytest.mark.asyncio
async def test_slide_outline_generation(mocker):
    """슬라이드 아웃라인 생성 테스트"""
    agent = StrategistAgent()
    outline_response = []
    for i in range(15):
        outline_response.append({
            "slide_number": i + 1,
            "slide_type": "title" if i == 0 else "content",
            "title": f"슬라이드 {i+1}",
            "headline": f"헤드라인 {i+1}",
            "content_type": "text",
            "key_points": [],
            "data_requirements": [],
            "layout_suggestion": "title_slide",
            "category": "intro"
        })
    mocker.patch.object(agent.llm_client, 'generate', return_value=json.dumps(outline_response))

    pyramid = {
        'top_message': '아시아 시장 진출로 3년 내 매출 30% 성장 실현',
        'supporting_arguments': []
    }
    framework = {'framework_name': '3C', 'categories': []}
    outline = await agent._create_slide_outline(pyramid, framework, 15)

    assert len(outline) == 15
    assert outline[0]['slide_type'] == 'title'

def test_framework_library():
    """프레임워크 라이브러리 테스트"""
    library = MECEFrameworkLibrary()
    framework = library.get_framework('3C')
    assert framework['name'] == '3C Analysis'
    frameworks = library.list_frameworks()
    assert '3C' in frameworks
    recommended = library.recommend_framework('시장 진출 전략')
    assert recommended == '3C'