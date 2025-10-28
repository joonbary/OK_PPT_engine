"""
맥킨지 수준 PPT 자동 생성 시스템
Multi-Agent LLM Architecture with FastAPI
"""

from fastapi import FastAPI, UploadFile, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
from enum import Enum
import json

# ================================
# 1. 시스템 아키텍처 설계
# ================================

class PPTGenerationSystem:
    """
    멀티 에이전트 기반 PPT 생성 시스템
    각 에이전트는 특정 역할을 담당
    """
    
    def __init__(self):
        self.agents = {
            "strategist": StrategistAgent(),      # 전략 및 구조 설계
            "analyst": DataAnalystAgent(),        # 데이터 분석 및 인사이트
            "storyteller": StorytellerAgent(),    # 스토리라인 구성
            "designer": DesignAgent(),            # 시각 디자인
            "reviewer": QualityReviewAgent()      # 품질 검토
        }
        
        self.workflow_engine = WorkflowEngine()
        self.template_library = TemplateLibrary()
        self.quality_scorer = QualityScorer()

# ================================
# 2. 멀티 에이전트 시스템
# ================================

class AgentRole(Enum):
    STRATEGIST = "strategist"
    ANALYST = "analyst"
    STORYTELLER = "storyteller"
    DESIGNER = "designer"
    REVIEWER = "reviewer"

class BaseAgent:
    """기본 에이전트 클래스"""
    
    def __init__(self, role: AgentRole):
        self.role = role
        self.llm_client = self._init_llm_client()
        self.system_prompt = self._load_system_prompt()
        
    def _init_llm_client(self):
        """LLM 클라이언트 초기화"""
        # Claude, GPT-4, 또는 오픈소스 모델 선택
        return LLMClient(
            model="claude-3-opus" if self.role == AgentRole.STRATEGIST 
            else "gpt-4-turbo"
        )
    
    def _load_system_prompt(self):
        """역할별 시스템 프롬프트 로드"""
        prompts = {
            AgentRole.STRATEGIST: """
            당신은 맥킨지 시니어 파트너입니다.
            MECE 원칙과 피라미드 구조를 적용하여
            전략적 프레젠테이션 구조를 설계합니다.
            """,
            
            AgentRole.ANALYST: """
            당신은 맥킨지의 데이터 분석 전문가입니다.
            데이터에서 전략적 인사이트를 도출하고
            적절한 시각화 방법을 제안합니다.
            """,
            
            AgentRole.STORYTELLER: """
            당신은 맥킨지의 커뮤니케이션 전문가입니다.
            SCR(상황-복잡성-해결) 구조로
            설득력 있는 스토리라인을 구성합니다.
            """,
            
            AgentRole.DESIGNER: """
            당신은 맥킨지의 비주얼 디자인 전문가입니다.
            깔끔하고 전문적인 슬라이드 디자인을 생성합니다.
            """,
            
            AgentRole.REVIEWER: """
            당신은 맥킨지 품질 검토 파트너입니다.
            So What 테스트와 품질 기준에 따라
            프레젠테이션을 검토하고 개선점을 제시합니다.
            """
        }
        return prompts[self.role]
    
    async def process(self, input_data: Dict, context: Dict) -> Dict:
        """에이전트 처리 메서드"""
        raise NotImplementedError

class StrategistAgent(BaseAgent):
    """전략 구조 설계 에이전트"""
    
    def __init__(self):
        super().__init__(AgentRole.STRATEGIST)
        
    async def process(self, input_data: Dict, context: Dict) -> Dict:
        """
        1. 문서 분석
        2. MECE 구조 생성
        3. 피라미드 원칙 적용
        4. 슬라이드 구조 설계
        """
        
        # 문서 내용 분석
        analysis = await self._analyze_document(input_data['document'])
        
        # MECE 프레임워크 선택
        framework = self._select_framework(analysis)
        
        # 피라미드 구조 생성
        pyramid = self._create_pyramid_structure(analysis, framework)
        
        # 슬라이드 아웃라인 생성
        outline = self._create_slide_outline(pyramid)
        
        return {
            "analysis": analysis,
            "framework": framework,
            "pyramid": pyramid,
            "outline": outline
        }
    
    async def _analyze_document(self, document: str) -> Dict:
        """문서 분석 및 핵심 요소 추출"""
        prompt = f"""
        다음 문서를 분석하여 핵심 요소를 추출하세요:
        
        {document}
        
        추출 항목:
        1. 핵심 메시지
        2. 주요 데이터 포인트
        3. 타겟 청중
        4. 목적
        5. 컨텍스트
        """
        
        response = await self.llm_client.generate(prompt)
        return json.loads(response)
    
    def _select_framework(self, analysis: Dict) -> str:
        """적절한 MECE 프레임워크 선택"""
        frameworks = {
            "market_entry": "3C",
            "competitive": "Porter5",
            "strategic": "SWOT",
            "operational": "7S",
            "marketing": "4P"
        }
        
        # 분석 결과에 기반하여 프레임워크 선택
        context_type = self._identify_context_type(analysis)
        return frameworks.get(context_type, "MECE_CUSTOM")

class DataAnalystAgent(BaseAgent):
    """데이터 분석 및 시각화 에이전트"""
    
    async def process(self, input_data: Dict, context: Dict) -> Dict:
        """
        1. 데이터 추출 및 정제
        2. 인사이트 도출
        3. 시각화 방법 결정
        4. 차트 사양 생성
        """
        
        # 데이터 추출
        data_points = self._extract_data(input_data)
        
        # 인사이트 도출
        insights = await self._generate_insights(data_points)
        
        # 시각화 매핑
        visualizations = self._map_to_visualizations(insights)
        
        return {
            "data_points": data_points,
            "insights": insights,
            "visualizations": visualizations
        }
    
    def _map_to_visualizations(self, insights: List[Dict]) -> List[Dict]:
        """인사이트별 최적 시각화 방법 결정"""
        
        chart_selector = {
            "comparison": self._select_comparison_chart,
            "trend": self._select_trend_chart,
            "composition": self._select_composition_chart,
            "distribution": self._select_distribution_chart,
            "relationship": self._select_relationship_chart
        }
        
        visualizations = []
        for insight in insights:
            insight_type = insight['type']
            chart_spec = chart_selector[insight_type](insight)
            visualizations.append(chart_spec)
            
        return visualizations

# ================================
# 3. 워크플로우 엔진
# ================================

class WorkflowEngine:
    """다단계 처리 파이프라인"""
    
    def __init__(self):
        self.stages = [
            "document_analysis",
            "structure_design",
            "content_generation",
            "design_application",
            "quality_review",
            "iteration"
        ]
        
    async def execute(self, input_data: Dict) -> Dict:
        """파이프라인 실행"""
        
        context = {"input": input_data}
        
        for stage in self.stages:
            stage_result = await self._execute_stage(stage, context)
            context[stage] = stage_result
            
            # 품질 체크
            if not self._quality_check(stage_result):
                # 재시도 또는 개선
                context[stage] = await self._improve_stage(stage, stage_result)
        
        return context
    
    async def _execute_stage(self, stage: str, context: Dict) -> Dict:
        """각 스테이지 실행"""
        
        stage_handlers = {
            "document_analysis": self._analyze_document,
            "structure_design": self._design_structure,
            "content_generation": self._generate_content,
            "design_application": self._apply_design,
            "quality_review": self._review_quality,
            "iteration": self._iterate_improvement
        }
        
        return await stage_handlers[stage](context)
    
    def _quality_check(self, result: Dict) -> bool:
        """스테이지 결과 품질 검증"""
        
        quality_metrics = {
            "completeness": result.get("completeness", 0),
            "coherence": result.get("coherence", 0),
            "relevance": result.get("relevance", 0)
        }
        
        # 모든 메트릭이 임계값 이상인지 확인
        threshold = 0.8
        return all(score >= threshold for score in quality_metrics.values())

# ================================
# 4. 템플릿 시스템
# ================================

class TemplateLibrary:
    """맥킨지 스타일 템플릿 라이브러리"""
    
    def __init__(self):
        self.templates = {
            "executive_summary": ExecutiveSummaryTemplate(),
            "market_analysis": MarketAnalysisTemplate(),
            "strategy_options": StrategyOptionsTemplate(),
            "implementation": ImplementationTemplate(),
            "financial_projection": FinancialProjectionTemplate()
        }
        
        self.layouts = {
            "title_slide": TitleSlideLayout(),
            "dual_header": DualHeaderLayout(),
            "three_column": ThreeColumnLayout(),
            "matrix": MatrixLayout(),
            "waterfall": WaterfallLayout()
        }
        
    def select_template(self, content_type: str) -> 'Template':
        """콘텐츠 유형에 맞는 템플릿 선택"""
        return self.templates.get(content_type)
    
    def select_layout(self, slide_type: str) -> 'Layout':
        """슬라이드 유형에 맞는 레이아웃 선택"""
        return self.layouts.get(slide_type)

class Template:
    """기본 템플릿 클래스"""
    
    def __init__(self):
        self.structure = self._define_structure()
        self.style_guide = self._define_style()
        
    def _define_structure(self) -> Dict:
        """템플릿 구조 정의"""
        raise NotImplementedError
    
    def _define_style(self) -> Dict:
        """스타일 가이드 정의"""
        return {
            "colors": {
                "primary": "#0076A8",
                "secondary": "#F47621",
                "text": "#53565A",
                "background": "#FFFFFF"
            },
            "fonts": {
                "title": {"family": "Arial", "size": 18, "weight": "bold"},
                "body": {"family": "Arial", "size": 14, "weight": "normal"},
                "caption": {"family": "Arial", "size": 10, "weight": "light"}
            }
        }
    
    def apply(self, content: Dict) -> Dict:
        """템플릿 적용"""
        raise NotImplementedError

# ================================
# 5. 품질 평가 시스템
# ================================

class QualityScorer:
    """PPT 품질 평가 시스템"""
    
    def __init__(self):
        self.criteria = {
            "clarity": 0.2,          # 명확성
            "insight": 0.25,         # 인사이트 깊이
            "structure": 0.2,        # 구조 논리성
            "visual": 0.15,          # 시각적 효과
            "actionability": 0.2     # 실행 가능성
        }
        
    def evaluate(self, presentation: Dict) -> Dict:
        """프레젠테이션 평가"""
        
        scores = {}
        
        # 각 기준별 평가
        scores["clarity"] = self._evaluate_clarity(presentation)
        scores["insight"] = self._evaluate_insight(presentation)
        scores["structure"] = self._evaluate_structure(presentation)
        scores["visual"] = self._evaluate_visual(presentation)
        scores["actionability"] = self._evaluate_actionability(presentation)
        
        # 가중 평균 계산
        total_score = sum(
            scores[criterion] * weight 
            for criterion, weight in self.criteria.items()
        )
        
        # 개선 제안 생성
        improvements = self._generate_improvements(scores)
        
        return {
            "scores": scores,
            "total_score": total_score,
            "improvements": improvements,
            "passed": total_score >= 0.8
        }
    
    def _evaluate_clarity(self, presentation: Dict) -> float:
        """명확성 평가"""
        
        checks = [
            self._check_headline_clarity,
            self._check_message_consistency,
            self._check_terminology_consistency
        ]
        
        return sum(check(presentation) for check in checks) / len(checks)
    
    def _check_headline_clarity(self, presentation: Dict) -> float:
        """헤드라인 명확성 체크"""
        
        headlines = [slide.get("headline", "") for slide in presentation["slides"]]
        
        # So What 테스트
        clear_headlines = sum(
            1 for headline in headlines
            if self._passes_so_what_test(headline)
        )
        
        return clear_headlines / len(headlines) if headlines else 0

# ================================
# 6. FastAPI 서버
# ================================

app = FastAPI(title="McKinsey-Level PPT Generation API")

class PPTRequest(BaseModel):
    """PPT 생성 요청 모델"""
    document: str
    style: str = "mckinsey"
    target_audience: str = "executive"
    num_slides: int = 15
    language: str = "ko"

class PPTResponse(BaseModel):
    """PPT 생성 응답 모델"""
    ppt_id: str
    status: str
    download_url: Optional[str]
    preview_url: Optional[str]
    quality_score: Optional[float]
    estimated_time: Optional[int]

@app.post("/generate-ppt", response_model=PPTResponse)
async def generate_ppt(
    request: PPTRequest,
    background_tasks: BackgroundTasks
):
    """PPT 생성 엔드포인트"""
    
    # 작업 ID 생성
    ppt_id = generate_unique_id()
    
    # 백그라운드 작업 추가
    background_tasks.add_task(
        process_ppt_generation,
        ppt_id,
        request
    )
    
    return PPTResponse(
        ppt_id=ppt_id,
        status="processing",
        estimated_time=300  # 5분 예상
    )

@app.get("/ppt-status/{ppt_id}")
async def get_ppt_status(ppt_id: str):
    """PPT 생성 상태 조회"""
    
    status = await get_generation_status(ppt_id)
    
    return {
        "ppt_id": ppt_id,
        "status": status.get("status"),
        "progress": status.get("progress"),
        "current_stage": status.get("current_stage"),
        "quality_score": status.get("quality_score"),
        "download_url": status.get("download_url")
    }

async def process_ppt_generation(ppt_id: str, request: PPTRequest):
    """PPT 생성 프로세스"""
    
    try:
        # 1. 시스템 초기화
        system = PPTGenerationSystem()
        
        # 2. 워크플로우 실행
        result = await system.workflow_engine.execute({
            "document": request.document,
            "style": request.style,
            "target_audience": request.target_audience,
            "num_slides": request.num_slides
        })
        
        # 3. PPT 파일 생성
        ppt_file = await generate_pptx_file(result)
        
        # 4. 품질 평가
        quality_score = system.quality_scorer.evaluate(result)
        
        # 5. 저장 및 URL 생성
        download_url = await save_and_get_url(ppt_file)
        
        # 6. 상태 업데이트
        await update_status(ppt_id, {
            "status": "completed",
            "download_url": download_url,
            "quality_score": quality_score["total_score"]
        })
        
    except Exception as e:
        await update_status(ppt_id, {
            "status": "failed",
            "error": str(e)
        })

# ================================
# 7. 반복적 개선 시스템
# ================================

class IterativeImprover:
    """반복적 개선 시스템"""
    
    def __init__(self):
        self.max_iterations = 3
        self.target_score = 0.85
        
    async def improve(self, presentation: Dict, feedback: Dict) -> Dict:
        """피드백 기반 개선"""
        
        iteration = 0
        current_score = feedback["total_score"]
        
        while iteration < self.max_iterations and current_score < self.target_score:
            # 개선 전략 선택
            strategy = self._select_improvement_strategy(feedback)
            
            # 개선 적용
            improved = await self._apply_improvements(presentation, strategy)
            
            # 재평가
            new_feedback = QualityScorer().evaluate(improved)
            
            if new_feedback["total_score"] > current_score:
                presentation = improved
                current_score = new_feedback["total_score"]
                feedback = new_feedback
            
            iteration += 1
        
        return presentation
    
    def _select_improvement_strategy(self, feedback: Dict) -> Dict:
        """개선 전략 선택"""
        
        # 가장 낮은 점수 영역 식별
        scores = feedback["scores"]
        weakest_area = min(scores, key=scores.get)
        
        strategies = {
            "clarity": self._improve_clarity_strategy,
            "insight": self._improve_insight_strategy,
            "structure": self._improve_structure_strategy,
            "visual": self._improve_visual_strategy,
            "actionability": self._improve_actionability_strategy
        }
        
        return strategies[weakest_area]()

# ================================
# 8. 고급 기능
# ================================

class AdvancedFeatures:
    """고급 기능 모음"""
    
    @staticmethod
    async def generate_speaker_notes(slides: List[Dict]) -> List[str]:
        """발표자 노트 자동 생성"""
        notes = []
        
        for slide in slides:
            note = f"""
            [슬라이드 {slide['number']}]
            
            핵심 메시지:
            {slide['headline']}
            
            주요 포인트:
            {' '.join(slide['key_points'])}
            
            전환 문구:
            {slide.get('transition', '다음 슬라이드로 넘어가겠습니다.')}
            
            예상 질문:
            {' '.join(slide.get('expected_questions', []))}
            """
            notes.append(note)
        
        return notes
    
    @staticmethod
    async def generate_executive_memo(presentation: Dict) -> str:
        """경영진 메모 생성"""
        
        memo = f"""
        주제: {presentation['title']}
        
        핵심 메시지:
        {presentation['key_message']}
        
        주요 발견:
        1. {presentation['findings'][0]}
        2. {presentation['findings'][1]}
        3. {presentation['findings'][2]}
        
        권고사항:
        {presentation['recommendations']}
        
        다음 단계:
        {presentation['next_steps']}
        """
        
        return memo

# ================================
# 실행
# ================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
