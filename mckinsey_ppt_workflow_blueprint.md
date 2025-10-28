# McKinsey PPT 자동 생성 시스템 - 단계별 워크플로우 UI 구축 Blueprint

> **대상**: Claude Code (개발 실행 AI)  
> **작성자 역할**: 풀스택 개발자 + 전문 UI/UX 디자이너  
> **프로젝트 경로**: `D:\PPT_Designer_OK`  
> **목표**: 5단계 워크플로우를 시각화하고 각 단계별로 디버깅 가능한 UI 구축

---

## 📋 프로젝트 컨텍스트

### 현재 상태
- ✅ **백엔드 완성도**: 85% (품질 점수 0.873 달성)
- ✅ **핵심 엔진 완료**: WorkflowOrchestrator, ContentGenerator, QualityController
- ⚠️ **UI 현황**: 백엔드만 존재, 프론트엔드 미구축
- 🎯 **다음 목표**: 단계별 워크플로우 UI 구축

### 개발 철학
```
"한 단계씩 완성 → 테스트 → 다음 단계"
각 단계가 독립적으로 실행/검증 가능해야 함
```

---

## 🎨 5단계 워크플로우 정의 (개선안)

### Stage 1: 문서 분석 (Document Analysis)
**목적**: 원천 데이터를 PPT 제작에 최적화된 형태로 전처리

**입력**:
- 업로드된 문서 (DOCX, PDF, TXT)
- 또는 직접 입력한 텍스트

**처리**:
1. 문서 파싱 및 텍스트 추출
2. 핵심 메시지 식별 (StrategistAgent)
3. 데이터 포인트 추출 (DataAnalystAgent)
4. 타겟 청중 및 목적 분석
5. **음슴체 변환** 및 구조화

**출력** (JSON):
```json
{
  "core_message": "아시아 시장이 3년 내 50% 성장 예상",
  "data_points": [
    {"type": "수치", "value": "50%", "context": "성장률"},
    {"type": "기간", "value": "3년", "context": "시간"}
  ],
  "key_topics": ["시장분석", "성장전략", "경쟁우위"],
  "target_audience": "C-Level 경영진",
  "tone": "전문적, 데이터 중심",
  "processed_content": "아시아 시장 매출이..."
}
```

**UI 요구사항**:
```
┌─────────────────────────────────────────┐
│  Stage 1: 문서 분석                      │
├─────────────────────────────────────────┤
│ [파일 업로드]  또는  [텍스트 직접 입력]  │
│                                          │
│ 📄 업로드된 파일: business_plan.docx     │
│ ⏱️ 분석 진행률: ████████░░ 80%          │
│                                          │
│ 🔍 분석 결과 미리보기:                   │
│ ┌────────────────────────────────────┐  │
│ │ • 핵심 메시지: "아시아 시장 50%..."  │  │
│ │ • 데이터 포인트: 12개 발견           │  │
│ │ • 주요 토픽: 시장분석, 성장전략...   │  │
│ └────────────────────────────────────┘  │
│                                          │
│ [✓ 분석 완료] [→ 다음 단계]              │
└─────────────────────────────────────────┘
```

---

### Stage 2: 구조 설계 (Structure Design)
**목적**: McKinsey 방법론에 따라 프레젠테이션 구조 설계

**입력**:
- Stage 1의 분석 결과
- 사용자 선택 옵션 (슬라이드 수, 스타일)

**처리**:
1. MECE 프레임워크 선택 (3C, 4P, SWOT, Porter's 5 Forces 등)
2. 피라미드 구조 생성
3. 슬라이드 개수 및 순서 결정
4. 각 슬라이드별 레이아웃 매핑
5. 스토리라인 구성 (SCR 구조)

**출력** (JSON):
```json
{
  "framework": "3C",
  "total_slides": 15,
  "story_structure": "SCR",
  "slide_outline": [
    {
      "slide_number": 1,
      "type": "title",
      "layout": "TitleSlide",
      "headline": "아시아 시장 진출 전략",
      "purpose": "프레젠테이션 주제 소개"
    },
    {
      "slide_number": 2,
      "type": "executive_summary",
      "layout": "DualHeader",
      "headline": "3개 핵심 인사이트가 50% 성장 가능성 시사",
      "purpose": "핵심 메시지 전달",
      "sub_sections": ["시장 기회", "경쟁 우위", "실행 전략"]
    },
    {
      "slide_number": 3,
      "type": "situation",
      "layout": "ThreeColumn",
      "headline": "아시아 시장이 연 15% 성장하며 기회 확대",
      "chart_type": "line_chart"
    }
  ]
}
```

**UI 요구사항**:
```
┌─────────────────────────────────────────┐
│  Stage 2: 구조 설계                      │
├─────────────────────────────────────────┤
│ 📊 선택된 프레임워크: 3C Analysis        │
│ 📑 슬라이드 구조: 15장                   │
│                                          │
│ 🎯 스토리라인 흐름:                      │
│ ┌────────────────────────────────────┐  │
│ │ 1. [Title] 아시아 시장 진출 전략    │  │
│ │ 2. [Summary] 3개 핵심 인사이트      │  │
│ │ 3. [Situation] 시장 기회 분석       │  │
│ │ 4. [Complication] 경쟁 환경         │  │
│ │ 5. [Resolution] 실행 전략           │  │
│ │ ... (더보기)                         │  │
│ └────────────────────────────────────┘  │
│                                          │
│ 🎨 레이아웃 미리보기:                    │
│ [Slide 2 - DualHeader 레이아웃 보기]    │
│                                          │
│ [← 이전 단계] [✓ 구조 확정] [→ 다음]    │
└─────────────────────────────────────────┘
```

---

### Stage 3: 콘텐츠 생성 (Content Generation)
**목적**: 설계된 구조에 맞는 고품질 콘텐츠 생성

**입력**:
- Stage 2의 슬라이드 구조
- Stage 1의 원천 데이터

**처리**:
1. HeadlineGenerator: McKinsey 4가지 패턴 헤드라인 생성
2. InsightLadder: 4단계 인사이트 생성
3. 본문 콘텐츠 생성 (음슴체)
4. 액션 아이템 생성 ([최우선]/[핵심]/[중요] 우선순위)
5. 차트 데이터 준비

**출력** (JSON):
```json
{
  "slides": [
    {
      "slide_number": 3,
      "headline": "아시아 시장이 2024-2027년 50% 성장하여 최대 기회 제공",
      "content": {
        "insight_level_1": "2024년 시장 규모 $100B",
        "insight_level_2": "전년 대비 15% 성장, 글로벌 평균 8% 대비 2배",
        "insight_level_3": "디지털 전환이 성장의 70% 주도",
        "insight_level_4": "디지털 영역 투자 확대로 추가 30% 성장 가능",
        "body_points": [
          "주요 성장 동인: 중산층 확대, 디지털화, 정부 지원",
          "경쟁사 대비 우위: 브랜드 인지도 30% 높음"
        ],
        "action_items": [
          "[최우선] 3개 핵심 시장 진출 가속화 (6개월 내)",
          "[핵심] 현지 파트너십 구축 50% 확대"
        ]
      },
      "chart_data": {
        "type": "line",
        "title": "시장 성장 추이",
        "data": {"2022": 87, "2023": 100, "2024": 115}
      }
    }
  ]
}
```

**UI 요구사항**:
```
┌─────────────────────────────────────────┐
│  Stage 3: 콘텐츠 생성                    │
├─────────────────────────────────────────┤
│ 🔄 생성 진행: Slide 3/15                 │
│ ⏱️ 예상 시간: 2분 30초 남음              │
│                                          │
│ 📝 현재 생성 중인 슬라이드:               │
│ ┌────────────────────────────────────┐  │
│ │ Slide 3: Situation                  │  │
│ │                                     │  │
│ │ 헤드라인: "아시아 시장이 2024-2027년"│  │
│ │ 50% 성장하여 최대 기회 제공"        │  │
│ │                                     │  │
│ │ 인사이트:                           │  │
│ │ • Level 1: 2024년 시장 $100B        │  │
│ │ • Level 2: 전년 대비 15% 성장       │  │
│ │ • Level 3: 디지털 전환 70% 주도     │  │
│ │ • Level 4: 투자 확대로 30% 추가성장 │  │
│ │                                     │  │
│ │ 액션 아이템:                        │  │
│ │ [최우선] 3개 핵심 시장 진출         │  │
│ └────────────────────────────────────┘  │
│                                          │
│ [⏸️ 일시정지] [✓ 생성 완료] [→ 다음]    │
└─────────────────────────────────────────┘
```

---

### Stage 4: 디자인 적용 (Design Application)
**목적**: McKinsey 스타일로 시각적 완성도 극대화

**입력**:
- Stage 3의 콘텐츠
- Stage 2의 레이아웃 정보

**처리**:
1. 템플릿 및 레이아웃 적용
2. 폰트, 색상, 여백 표준화 (McKinsey CI)
3. 차트 생성 및 스타일링
4. 중요 텍스트 강조 (Bold, 색상)
5. 인포그래픽 요소 추가
6. SlideValidator: 텍스트 오버플로우, 요소 겹침 검증
7. SlideFixer: 자동 수정 (95%+ 성공률)

**출력**:
- python-pptx Presentation 객체
- 미리보기 이미지 (PNG)

**UI 요구사항**:
```
┌─────────────────────────────────────────┐
│  Stage 4: 디자인 적용                    │
├─────────────────────────────────────────┤
│ 🎨 McKinsey 스타일 적용 중...            │
│                                          │
│ ✅ 템플릿 적용 완료                      │
│ ✅ 폰트/색상 표준화 완료                 │
│ 🔄 차트 생성 중... (8/12)                │
│ ⏳ 검증 대기 중...                       │
│                                          │
│ 📊 디자인 미리보기:                      │
│ ┌────────────────────────────────────┐  │
│ │  [Slide 1 썸네일]  [Slide 2]  ...  │  │
│ └────────────────────────────────────┘  │
│                                          │
│ 🔍 검증 결과:                            │
│ • 텍스트 오버플로우: 0건                 │
│ • 요소 겹침: 1건 → 자동 수정 완료        │
│ • 가독성: 100% 통과                      │
│                                          │
│ [🔄 재생성] [✓ 디자인 확정] [→ 다음]    │
└─────────────────────────────────────────┘
```

---

### Stage 5: 품질 검토 (Quality Review)
**목적**: McKinsey 기준으로 최종 품질 검증

**입력**:
- Stage 4의 완성된 PPT

**처리**:
1. QualityController 실행
2. 5가지 기준 평가:
   - Clarity (20%): So What 테스트
   - Insight (25%): 4단계 래더 도달
   - Structure (20%): MECE, 논리적 흐름
   - Visual (15%): 디자인 일관성
   - Actionability (20%): 실행 가능성
3. 개선 제안 생성
4. 반복 개선 (최대 3회, 목표: 0.85점)

**출력** (JSON):
```json
{
  "total_score": 0.873,
  "passed": true,
  "scores": {
    "clarity": 0.931,
    "insight": 0.800,
    "structure": 0.720,
    "visual": 0.950,
    "actionability": 1.000
  },
  "improvements": [
    {
      "area": "structure",
      "issue": "슬라이드 7-9의 논리적 연결 미흡",
      "suggestion": "전환 슬라이드 추가 권장"
    }
  ],
  "iteration_history": [
    {"iteration": 1, "score": 0.665},
    {"iteration": 2, "score": 0.821},
    {"iteration": 3, "score": 0.873}
  ]
}
```

**UI 요구사항**:
```
┌─────────────────────────────────────────┐
│  Stage 5: 품질 검토                      │
├─────────────────────────────────────────┤
│ 🏆 최종 품질 점수: 0.873 / 1.000         │
│ ✅ 목표 달성 (기준: 0.85)                │
│                                          │
│ 📊 세부 점수:                            │
│ ┌────────────────────────────────────┐  │
│ │ Clarity:        ████████░ 0.931    │  │
│ │ Insight:        ████████░ 0.800    │  │
│ │ Structure:      ███████░░ 0.720    │  │
│ │ Visual:         █████████ 0.950    │  │
│ │ Actionability:  ██████████ 1.000   │  │
│ └────────────────────────────────────┘  │
│                                          │
│ 💡 개선 제안:                            │
│ ┌────────────────────────────────────┐  │
│ │ ⚠️ Structure 영역:                  │  │
│ │ "슬라이드 7-9의 논리적 연결 미흡"   │  │
│ │ → 전환 슬라이드 추가 권장           │  │
│ └────────────────────────────────────┘  │
│                                          │
│ [🔄 재검토] [💾 저장] [📥 다운로드]      │
└─────────────────────────────────────────┘
```

---

## 🏗️ 기술 스택 및 아키텍처

### Frontend (UI Layer)
```yaml
Framework: Streamlit (빠른 프로토타입) 또는 React (프로덕션)
  
옵션 1 - Streamlit (권장):
  - 이유: Python 개발자 친화적, 빠른 개발, 백엔드 통합 용이
  - 단점: 커스터마이징 제한
  
옵션 2 - React + FastAPI:
  - 이유: 완전한 커스터마이징, 프로덕션 레디
  - 단점: 개발 시간 증가

추천: Streamlit으로 먼저 MVP 구축 → 필요시 React 전환
```

### Backend (기존 활용)
```python
# 이미 구축된 모듈들
app/
├── core/
│   ├── slide_validator.py      # Stage 4 검증
│   ├── slide_fixer.py          # Stage 4 자동 수정
│   └── text_fitter.py          # Stage 4 텍스트 최적화
├── services/
│   ├── workflow_orchestrator.py    # 전체 파이프라인 오케스트레이션
│   ├── content_generator.py        # Stage 3
│   ├── design_applicator.py        # Stage 4
│   ├── quality_controller.py       # Stage 5
│   ├── headline_generator.py       # Stage 3
│   └── insight_ladder.py           # Stage 3
└── agents/
    ├── strategist_agent.py         # Stage 1, 2
    ├── data_analyst_agent.py       # Stage 1, 3
    └── storyteller_agent.py        # Stage 2, 3
```

### 데이터 흐름
```
User Upload
    ↓
[Stage 1] → analysis_result.json
    ↓
[Stage 2] → structure_design.json
    ↓
[Stage 3] → content_generated.json
    ↓
[Stage 4] → presentation.pptx + preview.png
    ↓
[Stage 5] → quality_report.json
    ↓
Download PPT
```

---

## 📝 Claude Code 실행 계획 (Step-by-Step)

### Phase 1: Streamlit UI 기반 구조 (Week 1)

#### Step 1.1: 프로젝트 초기 설정
```bash
# 작업 디렉토리
cd D:\PPT_Designer_OK

# 새 디렉토리 생성
mkdir frontend
cd frontend

# 필수 패키지 설치
pip install streamlit streamlit-extras pillow python-docx PyPDF2
```

**생성할 파일**:
```
frontend/
├── app.py                      # 메인 앱
├── pages/
│   ├── 1_📄_문서분석.py
│   ├── 2_🏗️_구조설계.py
│   ├── 3_✍️_콘텐츠생성.py
│   ├── 4_🎨_디자인적용.py
│   └── 5_✅_품질검토.py
├── components/
│   ├── file_uploader.py
│   ├── progress_tracker.py
│   └── preview_renderer.py
└── utils/
    ├── session_state.py
    └── api_connector.py
```

#### Step 1.2: Stage 1 UI 구현
**파일**: `frontend/pages/1_📄_문서분석.py`

```python
import streamlit as st
import sys
sys.path.append('D:/PPT_Designer_OK')

from app.agents.strategist_agent import StrategistAgent
from app.agents.data_analyst_agent import DataAnalystAgent

st.set_page_config(page_title="Stage 1: 문서 분석", page_icon="📄")

st.title("📄 Stage 1: 문서 분석")
st.markdown("---")

# 파일 업로드
uploaded_file = st.file_uploader(
    "비즈니스 문서를 업로드하세요",
    type=['docx', 'pdf', 'txt'],
    help="지원 형식: DOCX, PDF, TXT"
)

# 또는 텍스트 직접 입력
text_input = st.text_area(
    "또는 텍스트를 직접 입력하세요",
    height=200,
    placeholder="여기에 비즈니스 내용을 입력하세요..."
)

if st.button("🔍 분석 시작", type="primary"):
    if uploaded_file or text_input:
        with st.spinner("문서 분석 중..."):
            # 문서 파싱
            if uploaded_file:
                content = parse_document(uploaded_file)
            else:
                content = text_input
            
            # StrategistAgent 실행
            strategist = StrategistAgent()
            analysis_result = strategist.analyze_document(content)
            
            # 세션에 저장
            st.session_state['stage1_result'] = analysis_result
            
        # 결과 표시
        st.success("✅ 분석 완료!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 핵심 메시지")
            st.info(analysis_result['core_message'])
            
            st.subheader("📊 데이터 포인트")
            for dp in analysis_result['data_points'][:5]:
                st.write(f"• {dp['type']}: {dp['value']} ({dp['context']})")
        
        with col2:
            st.subheader("🔑 주요 토픽")
            for topic in analysis_result['key_topics']:
                st.write(f"• {topic}")
            
            st.subheader("👥 타겟 청중")
            st.write(analysis_result['target_audience'])
        
        # 다음 단계 버튼
        if st.button("→ Stage 2로 이동", type="primary"):
            st.switch_page("pages/2_🏗️_구조설계.py")
    else:
        st.error("⚠️ 파일을 업로드하거나 텍스트를 입력하세요")
```

#### Step 1.3: 진행률 추적 컴포넌트
**파일**: `frontend/components/progress_tracker.py`

```python
import streamlit as st

def render_progress_tracker(current_stage: int):
    """5단계 진행률 표시"""
    stages = [
        {"num": 1, "name": "문서분석", "icon": "📄"},
        {"num": 2, "name": "구조설계", "icon": "🏗️"},
        {"num": 3, "name": "콘텐츠생성", "icon": "✍️"},
        {"num": 4, "name": "디자인적용", "icon": "🎨"},
        {"num": 5, "name": "품질검토", "icon": "✅"}
    ]
    
    # 프로그레스 바
    progress = current_stage / 5
    st.progress(progress)
    
    # 단계별 아이콘 표시
    cols = st.columns(5)
    for i, stage in enumerate(stages):
        with cols[i]:
            if stage['num'] < current_stage:
                st.markdown(f"✅ {stage['icon']}")
            elif stage['num'] == current_stage:
                st.markdown(f"🔄 {stage['icon']}")
            else:
                st.markdown(f"⏳ {stage['icon']}")
            st.caption(stage['name'])
```

---

### Phase 2: 나머지 Stage UI 구현 (Week 2-3)

#### Step 2.1: Stage 2 UI (구조 설계)
**핵심 기능**:
- MECE 프레임워크 선택 UI
- 슬라이드 아웃라인 트리뷰
- 레이아웃 미리보기
- 드래그 앤 드롭으로 순서 조정

#### Step 2.2: Stage 3 UI (콘텐츠 생성)
**핵심 기능**:
- 실시간 생성 진행률 표시
- 슬라이드별 콘텐츠 미리보기
- 수동 편집 가능
- 인사이트 래더 시각화

#### Step 2.3: Stage 4 UI (디자인 적용)
**핵심 기능**:
- 슬라이드 썸네일 그리드
- 클릭하여 상세 보기
- 검증 결과 실시간 표시
- 자동 수정 로그

#### Step 2.4: Stage 5 UI (품질 검토)
**핵심 기능**:
- 레이더 차트로 5가지 기준 시각화
- 개선 제안 리스트
- 반복 개선 이력
- 최종 다운로드 버튼

---

## 🎯 우선순위 및 실행 순서

### Week 1: MVP 구축
```
Day 1-2: Step 1.1, 1.2 (Stage 1 UI)
Day 3-4: Step 1.3 + Stage 2 UI 기본
Day 5: 통합 테스트 및 디버깅
```

### Week 2: 핵심 기능 완성
```
Day 1-2: Stage 3 UI
Day 3-4: Stage 4 UI
Day 5: Stage 5 UI
```

### Week 3: 최적화 및 배포
```
Day 1-2: 성능 최적화, 에러 핸들링
Day 3-4: UI/UX 개선, 사용자 테스트
Day 5: 문서화 및 배포
```

---

## 📋 체크리스트 (Claude Code 실행 전)

### 환경 확인
- [ ] Python 3.9+ 설치 확인
- [ ] `D:\PPT_Designer_OK` 경로 접근 가능
- [ ] 필수 패키지 설치 (requirements.txt 확인)
- [ ] 기존 백엔드 모듈 정상 작동 확인

### 개발 준비
- [ ] Streamlit 설치: `pip install streamlit`
- [ ] 개발 브랜치 생성: `git checkout -b feature/workflow-ui`
- [ ] .gitignore 업데이트 (Streamlit 캐시 제외)

### 실행 테스트
```bash
# Streamlit 앱 실행
cd D:\PPT_Designer_OK\frontend
streamlit run app.py

# 브라우저에서 http://localhost:8501 열림
```

---

## 🚨 주의사항 및 베스트 프랙티스

### 1. 세션 상태 관리
```python
# 각 단계의 결과를 세션에 저장
if 'stage1_result' not in st.session_state:
    st.session_state['stage1_result'] = None

# 다음 단계로 넘어가기 전 검증
if st.session_state['stage1_result'] is None:
    st.error("⚠️ Stage 1을 먼저 완료하세요")
    st.stop()
```

### 2. 에러 핸들링
```python
try:
    result = agent.process(data)
except Exception as e:
    st.error(f"❌ 처리 중 오류: {str(e)}")
    st.exception(e)  # 디버깅용 상세 에러
    st.stop()
```

### 3. 성능 최적화
```python
# 비용 절약: LLM 결과 캐싱
@st.cache_data
def analyze_document(content):
    return strategist.analyze(content)

# 파일 업로드 크기 제한
uploaded_file = st.file_uploader(
    "파일 업로드",
    type=['docx', 'pdf'],
    help="최대 10MB"
)
if uploaded_file and uploaded_file.size > 10 * 1024 * 1024:
    st.error("파일 크기가 10MB를 초과합니다")
```

### 4. 디버깅 모드
```python
# 개발자 모드 토글
if st.sidebar.checkbox("🔧 디버그 모드"):
    st.sidebar.json(st.session_state)
    st.sidebar.write("분석 결과:", analysis_result)
```

---

## 💡 추가 개선 아이디어

### 단기 (1-2주)
1. **자동 저장**: 각 단계 완료 시 자동으로 결과 저장
2. **히스토리**: 이전 작업 불러오기 기능
3. **템플릿 라이브러리**: 자주 사용하는 구조 저장

### 중기 (1개월)
1. **실시간 협업**: 여러 사용자 동시 작업
2. **버전 관리**: 수정 이력 추적
3. **A/B 테스트**: 여러 버전 생성 후 비교

### 장기 (3개월)
1. **AI 어시스턴트**: 챗봇으로 대화하며 PPT 생성
2. **음성 입력**: 음성으로 콘텐츠 입력
3. **자동 발표자 노트**: TTS로 스크립트 생성

---

## 📞 문제 발생 시 대응

### 일반적인 문제
1. **"ModuleNotFoundError"**
   → `pip install -r requirements.txt` 재실행

2. **"Streamlit 앱이 안 열림"**
   → 포트 충돌 확인: `streamlit run app.py --server.port 8502`

3. **"LLM API 오류"**
   → API 키 확인: `.env` 파일 점검

### 디버깅 팁
```python
# 로그 추가
import logging
logging.basicConfig(level=logging.DEBUG)

# Streamlit 디버그 정보
st.write("Session State:", st.session_state)
st.write("Current Stage:", current_stage)
```

---

**다음 작업**: 
위 Blueprint를 참고하여 `Step 1.1`부터 차근차근 구현하세요.
각 Step 완료 후 체크리스트를 업데이트하고 다음 단계로 진행합니다.

**질문이 있다면**:
- "Step 1.2의 `parse_document` 함수 구현 방법?"
- "Stage 2 UI에서 드래그 앤 드롭 기능 추가 방법?"
- 등 구체적으로 물어보세요!
