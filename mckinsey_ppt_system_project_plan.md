# 맥킨지 수준 PPT 자동 생성 시스템 - 프로젝트 분석 및 실행 계획

## 📌 프로젝트 개요

### 프로젝트 목표
FastAPI 기반의 멀티 에이전트 시스템을 구축하여 맥킨지 수준의 전문 컨설팅 PPT를 자동으로 생성하는 시스템 개발

### 핵심 특징
- **5개 특화 AI 에이전트**: Strategist, DataAnalyst, Storyteller, Designer, QualityReviewer
- **맥킨지 방법론 적용**: MECE 구조, 피라미드 원칙, So What 테스트
- **성능 목표**: 5분 내 15장 PPT 생성
- **품질 기준**: 0.85 이상의 품질 점수 달성

---

## 🏗️ 시스템 아키텍처

### 1. 전체 아키텍처 구조

```
┌─────────────────────────────────────────────────────────┐
│                   API Gateway Layer                      │
│                    (FastAPI Server)                      │
└─────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────┐
│               Agent Orchestration Layer                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Strategist│ │ Analyst  │ │Storyteller│ │ Designer │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│                    ┌──────────────┐                     │
│                    │Quality Review│                     │
│                    └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────┐
│                  Workflow Engine                         │
│     [Document Analysis → Structure Design →              │
│      Content Generation → Design Application →           │
│      Quality Review → Iteration]                         │
└─────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────┐
│            Template & Styling Layer                      │
│   [McKinsey Templates] [Layouts] [Chart Library]        │
└─────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────┐
│              Data & Storage Layer                        │
│      [PostgreSQL] [Redis Cache] [File Storage]          │
└─────────────────────────────────────────────────────────┘
```

### 2. 핵심 컴포넌트 상세

#### 2.1 Agent System (에이전트 시스템)

**BaseAgent 추상 클래스**
- LLM 클라이언트 초기화 및 관리
- 시스템 프롬프트 관리
- 공통 처리 로직

**5개 특화 에이전트**

| 에이전트 | LLM 모델 | 주요 역할 |
|---------|----------|-----------|
| StrategistAgent | Claude-3-Opus | MECE 구조 설계, 피라미드 원칙 적용 |
| DataAnalystAgent | GPT-4 Turbo | 데이터 추출, 인사이트 도출, 차트 선택 |
| StorytellerAgent | GPT-4 Turbo | SCR 구조 스토리라인, 내러티브 구성 |
| DesignAgent | GPT-4 Turbo | 시각 디자인, 레이아웃 적용 |
| QualityReviewAgent | GPT-4 Turbo | So What 테스트, 품질 검증 |

#### 2.2 Workflow Engine

**6단계 파이프라인**
1. **Document Analysis**: 문서 분석 및 핵심 요소 추출
2. **Structure Design**: MECE 구조 및 슬라이드 아웃라인 설계
3. **Content Generation**: 콘텐츠 생성 및 데이터 시각화
4. **Design Application**: 템플릿 및 스타일 적용
5. **Quality Review**: 품질 평가 및 검증
6. **Iteration**: 반복 개선 (최대 3회)

#### 2.3 Template System

**맥킨지 표준 템플릿**
- ExecutiveSummary
- MarketAnalysis
- StrategyOptions
- Implementation
- FinancialProjection

**레이아웃 시스템**
- TitleSlide
- DualHeader
- ThreeColumn
- Matrix
- Waterfall

#### 2.4 Quality Scoring System

**평가 기준 및 가중치**
- Clarity (명확성): 20%
- Insight (인사이트): 25%
- Structure (구조): 20%
- Visual (시각효과): 15%
- Actionability (실행가능성): 20%

---

## 🛠️ 기술 스택

### Backend Framework
- **FastAPI**: 비동기 웹 프레임워크
- **Pydantic**: 데이터 검증 및 설정 관리
- **asyncio**: 비동기 프로그래밍

### LLM Integration
- **Claude-3-Opus**: 전략 분석 (Strategist Agent)
- **GPT-4 Turbo**: 기타 에이전트
- **LangChain** (선택사항): LLM 오케스트레이션

### PPT Generation
- **python-pptx**: PowerPoint 파일 생성
- **Pillow**: 이미지 처리
- **matplotlib/plotly**: 차트 생성

### Database & Cache
- **PostgreSQL**: 메타데이터 및 작업 상태
- **Redis**: LLM 응답 캐싱, 세션 관리

### Background Tasks
- **Celery**: 비동기 작업 큐
- **RabbitMQ/Redis**: 메시지 브로커

### Development & Deployment
- **Docker**: 컨테이너화
- **Docker Compose**: 개발 환경
- **pytest**: 테스트 프레임워크
- **uvicorn**: ASGI 서버

---

## 📋 작업 분해 구조 (Work Breakdown Structure)

### Phase 1: 기초 인프라 구축 (Week 1-2)

#### Task 1: 프로젝트 기초 인프라 구축
**ID:** `749f3b90-3b61-423c-9db6-d8ea90bb7ce9`

**구현 내용:**
- FastAPI 애플리케이션 초기화
- 프로젝트 디렉토리 구조 설정
- 데이터베이스 연결 설정 (PostgreSQL, Redis)
- 환경 변수 관리 시스템
- 로깅 시스템 구축 (loguru)
- 에러 핸들링 미들웨어
- CORS 설정

**디렉토리 구조:**
```
/project-root
├── /app
│   ├── /api           # API 엔드포인트
│   ├── /agents        # 에이전트 모듈
│   ├── /core          # 핵심 설정, 보안
│   ├── /models        # Pydantic 모델
│   ├── /services      # 비즈니스 로직
│   ├── /templates     # PPT 템플릿
│   └── /utils         # 유틸리티 함수
├── /tests             # 테스트 코드
├── /docker            # Docker 설정
├── requirements.txt
├── .env.example
└── docker-compose.yml
```

**검증 기준:**
- FastAPI 서버 localhost:8000 실행
- Swagger UI (/docs) 접근 가능
- 데이터베이스 연결 테스트 통과

---

#### Task 2: LLM 통합 및 BaseAgent 구현
**ID:** `bb769b94-7564-48cf-964c-4d003d5dd55c`

**구현 내용:**
- BaseAgent 추상 클래스 구현
- LLMClient 클래스 개발
  - API 키 관리
  - 재시도 로직 (tenacity 라이브러리)
  - 응답 파싱 및 검증
  - 토큰 카운팅 및 비용 추적
- Redis 캐싱 레이어
- Rate limiting 구현

**코드 구조:**
```python
class BaseAgent(ABC):
    def __init__(self, role: AgentRole):
        self.role = role
        self.llm_client = self._init_llm_client()
        self.system_prompt = self._load_system_prompt()
    
    @abstractmethod
    async def process(self, input_data: Dict, context: Dict) -> Dict:
        pass

class LLMClient:
    def __init__(self, model: str):
        self.model = model
        self.cache = RedisCache()
        
    async def generate(self, prompt: str) -> str:
        # 캐시 확인
        # API 호출
        # 재시도 로직
        # 응답 파싱
        pass
```

**검증 기준:**
- LLM API 호출 성공
- 캐싱 동작 확인
- 재시도 메커니즘 작동

---

### Phase 2: 핵심 에이전트 개발 (Week 3-4)

#### Task 3: 5개 특화 에이전트 구현
**ID:** `5448015f-dfe6-4cd0-9b5a-270029f64f75`

**각 에이전트별 구현 상세:**

**StrategistAgent (전략가)**
- MECE 프레임워크 선택 로직
  - 3C (Company, Competitors, Customers)
  - 4P (Product, Price, Place, Promotion)
  - SWOT, Porter's 5 Forces, 7S
- 피라미드 구조 생성
- 슬라이드 아웃라인 설계

**DataAnalystAgent (분석가)**
- 데이터 추출 및 정제
- 통계 분석 및 트렌드 식별
- 인사이트 도출 (4단계 래더)
  - Observation → Comparison → Implication → Action
- 차트 타입 자동 선택

**StorytellerAgent (스토리텔러)**
- SCR (Situation-Complication-Resolution) 구조
- 내러티브 흐름 구성
- 전환 문구 생성
- Ghost Deck 방법론 적용

**DesignAgent (디자이너)**
- 레이아웃 선택 및 적용
- 색상 팔레트 관리
- 폰트 시스템 적용
- 시각적 계층 구조 설정

**QualityReviewAgent (품질 검토자)**
- So What 테스트 실행
- MECE 원칙 검증
- 정량화 검증
- 개선 제안 생성

**검증 기준:**
- 각 에이전트 단위 테스트 통과
- process() 메서드 출력 검증
- 에이전트 간 데이터 전달 확인

---

#### Task 4: 워크플로우 엔진 개발
**ID:** `514d56ea-1c91-4aca-ba33-164804055046`

**구현 내용:**
- WorkflowEngine 클래스
- 6단계 파이프라인 구현
- 단계별 체크포인트
- 컨텍스트 관리
- 에러 핸들링 및 재시도
- 병렬 처리 최적화 (asyncio.gather)

**파이프라인 상세:**
```python
class WorkflowEngine:
    stages = [
        "document_analysis",
        "structure_design", 
        "content_generation",
        "design_application",
        "quality_review",
        "iteration"
    ]
    
    async def execute(self, input_data: Dict) -> Dict:
        context = {"input": input_data}
        
        for stage in self.stages:
            stage_result = await self._execute_stage(stage, context)
            
            if not self._quality_check(stage_result):
                stage_result = await self._improve_stage(stage, stage_result)
                
            context[stage] = stage_result
            
        return context
```

**검증 기준:**
- 전체 파이프라인 E2E 실행
- 단계별 출력 검증
- 품질 체크포인트 동작 확인

---

### Phase 3: 템플릿 및 생성 엔진 (Week 5)

#### Task 5: 맥킨지 스타일 템플릿 시스템 구축
**ID:** `2c328cd3-14b7-45a2-af46-ff2e9314c412`

**템플릿 구현:**
- Template 기본 클래스
- 5개 전문 템플릿
  - ExecutiveSummaryTemplate
  - MarketAnalysisTemplate
  - StrategyOptionsTemplate
  - ImplementationTemplate
  - FinancialProjectionTemplate
- 5개 레이아웃 타입
  - TitleSlideLayout
  - DualHeaderLayout
  - ThreeColumnLayout
  - MatrixLayout
  - WaterfallLayout

**스타일 가이드:**
```yaml
colors:
  primary: "#0076A8"      # McKinsey Blue
  secondary: "#F47621"    # Emphasis Orange
  text: "#53565A"         # Neutral Gray
  positive: "#6BA644"     # Green
  negative: "#E31B23"     # Red

fonts:
  title: 
    size: 18pt
    weight: bold
  body:
    size: 14pt
    weight: normal
  caption:
    size: 10pt
    weight: light
```

**검증 기준:**
- 맥킨지 스타일 가이드 준수
- 템플릿 렌더링 테스트
- 레이아웃 적용 확인

---

#### Task 6: python-pptx PPT 생성 엔진 개발
**ID:** `b63e7e60-4841-4de0-91ae-c294c6559f5f`

**구현 내용:**
- PPTGenerator 클래스
- 슬라이드 생성 및 관리
- 텍스트/이미지/차트 삽입
- 차트 생성 모듈
  - 막대/선/파이 차트
  - 워터폴 차트
  - 히트맵 매트릭스
- 레이아웃 적용 엔진
- 파일 저장 및 스트리밍

**차트 생성 예시:**
```python
class ChartGenerator:
    def create_waterfall_chart(self, data: Dict) -> Chart:
        # 시작점
        # 긍정적 요인들
        # 부정적 요인들
        # 최종 결과
        pass
    
    def create_heatmap_matrix(self, data: Dict) -> Chart:
        # 행/열 매트릭스
        # 색상 스케일
        # 주석 추가
        pass
```

**검증 기준:**
- PPTX 파일 생성 성공
- PowerPoint에서 정상 열림
- 모든 요소 정확한 렌더링

---

### Phase 4: 품질 보증 및 API (Week 6)

#### Task 7: 품질 평가 및 개선 시스템
**ID:** `a3fe66e5-eaae-4811-b866-c1dd262caeb2`

**구현 내용:**
- QualityScorer 클래스
- 5개 평가 기준 구현
- 가중 평균 계산
- IterativeImprover 클래스
- 개선 전략 선택
- 반복 개선 메커니즘

**평가 메트릭:**
```python
criteria = {
    "clarity": 0.2,          # 명확성
    "insight": 0.25,         # 인사이트 깊이
    "structure": 0.2,        # 구조 논리성
    "visual": 0.15,          # 시각적 효과
    "actionability": 0.2     # 실행 가능성
}
```

**검증 기준:**
- 품질 점수 0-1 범위 계산
- 개선 제안 생성
- 반복 개선 동작 확인

---

#### Task 8: API 엔드포인트 및 백그라운드 작업
**ID:** `9ebdde29-3887-4fee-93c1-6ede745b1421`

**API 엔드포인트:**
```python
@app.post("/generate-ppt")
async def generate_ppt(request: PPTRequest) -> PPTResponse:
    # PPT 생성 작업 큐에 추가
    pass

@app.get("/ppt-status/{ppt_id}")
async def get_ppt_status(ppt_id: str) -> StatusResponse:
    # 생성 상태 조회
    pass

@app.get("/download/{ppt_id}")
async def download_ppt(ppt_id: str) -> FileResponse:
    # PPT 파일 다운로드
    pass
```

**Celery 작업:**
- PPT 생성 태스크
- 진행 상황 추적
- 결과 저장

**검증 기준:**
- API 엔드포인트 동작
- 비동기 작업 처리
- 파일 다운로드 성공

---

## 📊 프로젝트 일정 및 마일스톤

### 전체 일정 (6주)

```
Week 1-2: 기초 인프라 및 LLM 통합
├── Task 1: 프로젝트 기초 인프라 구축
├── Task 2: LLM 통합 및 BaseAgent 구현
└── Task 5: 맥킨지 스타일 템플릿 시스템 (병렬 진행)

Week 3-4: 핵심 에이전트 개발
├── Task 3: 5개 특화 에이전트 구현
└── Task 4: 워크플로우 엔진 개발 (Week 4)

Week 5: 템플릿 및 생성 엔진
├── Task 6: python-pptx PPT 생성 엔진
└── Task 7: 품질 평가 및 개선 시스템 (병렬 진행)

Week 6: API 및 통합 테스트
├── Task 8: API 엔드포인트 및 백그라운드 작업
├── 통합 테스트
└── 성능 최적화
```

### 주요 마일스톤

| 마일스톤 | 완료 시점 | 성공 기준 |
|---------|-----------|-----------|
| M1: 인프라 구축 완료 | Week 2 | FastAPI 서버 실행, LLM 연결 성공 |
| M2: 에이전트 시스템 완성 | Week 4 | 5개 에이전트 모두 동작, 워크플로우 실행 |
| M3: PPT 생성 가능 | Week 5 | 실제 PPTX 파일 생성 성공 |
| M4: 품질 기준 달성 | Week 6 | 품질 점수 0.85 이상 |
| M5: API 완성 | Week 6 | 5분 내 PPT 생성 목표 달성 |

---

## 🎯 성공 지표 (KPIs)

### 성능 지표
- **생성 시간**: 5분 이내 (15장 기준)
- **동시 처리**: 10개 이상 동시 요청 처리
- **응답 시간**: API 응답 < 200ms
- **가용성**: 99.9% 업타임

### 품질 지표
- **품질 점수**: 0.85 이상
- **So What 테스트**: 100% 통과
- **MECE 구조**: 모든 슬라이드 적용
- **정량화율**: 80% 이상 데이터 기반

### 비용 효율성
- **LLM API 비용**: 월 $500 이하
- **캐시 적중률**: 50% 이상
- **리소스 사용**: CPU < 70%, Memory < 4GB

---

## 🚨 리스크 관리

### 식별된 리스크 및 완화 전략

| 리스크 | 영향도 | 가능성 | 완화 전략 |
|--------|--------|--------|-----------|
| LLM API 응답 불일치 | 높음 | 중간 | 프롬프트 엔지니어링, 응답 검증 로직 |
| 5분 목표 미달성 | 높음 | 중간 | 캐싱, 병렬 처리, 프리로딩 |
| 품질 기준 미달 | 높음 | 낮음 | 반복 개선, A/B 테스트 |
| API 비용 초과 | 중간 | 중간 | Rate limiting, 예산 알림 |
| 확장성 문제 | 중간 | 낮음 | 마이크로서비스 아키텍처 |

### 컨틴전시 계획
1. **LLM 대체 모델**: Llama 3, Mistral 등 오픈소스 모델 준비
2. **성능 플랜 B**: 템플릿 기반 빠른 생성 모드
3. **비용 플랜 B**: 자체 호스팅 LLM 전환

---

## 💡 최적화 전략

### 즉시 적용 가능한 최적화

1. **LLM 응답 캐싱**
   - 유사 요청 감지 알고리즘
   - TTL 기반 캐시 무효화
   - Redis 캐시 활용

2. **비동기 처리 강화**
   - asyncio.gather()로 병렬 에이전트 실행
   - 스트리밍 응답으로 체감 속도 개선
   - WebSocket으로 실시간 진행률

3. **템플릿 최적화**
   - 자주 사용되는 템플릿 프리컴파일
   - 레이아웃 캐시 풀
   - 정적 요소 사전 렌더링

### 중장기 개선 방향

1. **자체 호스팅 LLM**
   - 온프레미스 배포로 비용 절감
   - 데이터 보안 강화
   - 커스터마이징 가능

2. **머신러닝 기반 개선**
   - 사용자 피드백 학습
   - Fine-tuning 데이터셋 구축
   - 품질 예측 모델

3. **실시간 협업 기능**
   - 다중 사용자 동시 편집
   - 버전 관리
   - 변경 이력 추적

---

## 🔧 개발 환경 설정

### 필수 요구사항
```bash
# Python 버전
Python 3.9+

# 주요 패키지
fastapi==0.104.1
pydantic==2.4.2
python-pptx==0.6.21
langchain==0.0.340
redis==5.0.1
celery==5.3.4
postgresql==15.0
```

### Docker Compose 설정
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/ppt_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
      
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=ppt_db
      
  redis:
    image: redis:7-alpine
    
  celery:
    build: .
    command: celery -A app.tasks worker --loglevel=info
    depends_on:
      - redis
```

### 환경 변수 (.env)
```env
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_claude_key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ppt_db
REDIS_URL=redis://localhost:6379

# Application
APP_ENV=development
LOG_LEVEL=INFO
MAX_WORKERS=4
PPT_GENERATION_TIMEOUT=300

# LLM Settings
LLM_CACHE_TTL=3600
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

---

## 📚 참고 자료

### 핵심 문서
1. **McKinsey_Style_PPT_Guidelines.md** - 맥킨지 스타일 가이드
2. **PPT_Layout_Analysis_and_Improvements.md** - 레이아웃 분석 및 개선
3. **mckinsey_ppt_system_architecture.py** - 시스템 아키텍처 코드

### 외부 참고 자료
- "The Pyramid Principle" - Barbara Minto
- "The McKinsey Way" - Ethan Rasiel
- "Say It With Charts" - Gene Zelazny
- McKinsey Insights (공식 웹사이트)
- FastAPI 공식 문서
- python-pptx 문서

### 기술 문서
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Celery Documentation](https://docs.celeryq.dev/)

---

## ✅ 체크리스트

### 프로젝트 시작 전
- [ ] Python 3.9+ 설치
- [ ] Docker & Docker Compose 설치
- [ ] PostgreSQL & Redis 설정
- [ ] API 키 획득 (OpenAI, Anthropic)
- [ ] 개발 환경 설정

### 개발 단계별
- [ ] Week 1-2: 기초 인프라 구축
- [ ] Week 3-4: 에이전트 시스템 개발
- [ ] Week 5: 템플릿 및 생성 엔진
- [ ] Week 6: API 및 통합 테스트

### 품질 검증
- [ ] 단위 테스트 작성 (coverage > 80%)
- [ ] 통합 테스트 수행
- [ ] 성능 테스트 (5분 목표)
- [ ] 품질 점수 검증 (0.85 이상)
- [ ] 보안 검토

### 배포 준비
- [ ] Production 환경 설정
- [ ] CI/CD 파이프라인
- [ ] 모니터링 설정
- [ ] 백업 전략
- [ ] 문서화 완성

---

## 📞 연락처 및 지원

### 프로젝트 관리
- **프로젝트 매니저**: [PM 이름]
- **기술 리드**: [Tech Lead 이름]
- **품질 관리**: [QA Lead 이름]

### 기술 지원
- **Slack 채널**: #ppt-generation-system
- **이슈 트래커**: GitHub Issues
- **문서 저장소**: Confluence/Notion

---

*마지막 업데이트: 2025년 1월 2일*
*버전: 1.0.0*
