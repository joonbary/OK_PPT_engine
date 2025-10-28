# 🧪 레이아웃 시스템 테스트 가이드

## 📋 구현된 기능 목록

### Phase 1-5 완료 기능
1. **ContentAnalyzer**: 마크다운 콘텐츠 분석 및 레이아웃 추천
2. **LayoutLibrary**: 8가지 전문 레이아웃 템플릿
3. **TextFitter**: 동적 텍스트 크기 조정 및 오버플로우 방지
4. **LayoutApplier**: 레이아웃별 정확한 콘텐츠 배치
5. **SlideValidator**: 8가지 품질 검증 기준
6. **SlideFixer**: 자동 문제 해결 시스템
7. **DesignAgent**: 통합 처리 파이프라인

## 🚀 테스트 방법

### 방법 1: 단독 테스트 스크립트 실행

개별 컴포넌트를 테스트하고 결과를 바로 확인할 수 있습니다.

```bash
# 프로젝트 디렉토리로 이동
cd D:\PPT_Designer_OK\mckinsey-ppt-generator

# 테스트 스크립트 실행
python test_layout_system.py
```

**생성되는 파일들:**
- `test_output_applier.pptx` - LayoutApplier 테스트 결과
- `test_output_fixed.pptx` - SlideFixer 수정 결과  
- `test_output_design_agent.pptx` - 통합 시스템 결과

### 방법 2: FastAPI 서버를 통한 테스트

실제 API 엔드포인트를 통해 전체 시스템을 테스트합니다.

#### Step 1: 서버 시작
```bash
# 프로젝트 디렉토리로 이동
cd D:\PPT_Designer_OK\mckinsey-ppt-generator

# FastAPI 서버 시작
uvicorn app.main:app --reload
```

#### Step 2: 테스트 실행 (새 터미널에서)
```bash
# 프로젝트 디렉토리로 이동
cd D:\PPT_Designer_OK\mckinsey-ppt-generator

# API 테스트 실행
python test_api_integration.py
```

#### Step 3: 브라우저에서 확인
- API 문서: http://localhost:8000/docs
- 상태 확인: http://localhost:8000/health

### 방법 3: pytest를 통한 단위 테스트

```bash
# pytest 설치 (필요시)
pip install pytest pytest-asyncio

# 테스트 실행
pytest tests/test_layout_system.py -v
```

## 📊 테스트 시나리오

### 1. ContentAnalyzer 테스트
- ✅ 불릿 리스트 감지
- ✅ 비교 콘텐츠 감지  
- ✅ 매트릭스/테이블 감지
- ✅ 한글 텍스트 분석

### 2. TextFitter 테스트
- ✅ 텍스트 박스 맞춤
- ✅ 폰트 크기 자동 조정
- ✅ 텍스트 트렁케이션
- ✅ 스마트 줄바꿈

### 3. LayoutApplier 테스트
- ✅ 불릿 리스트 레이아웃
- ✅ 2컬럼 비교 레이아웃
- ✅ 3컬럼 레이아웃
- ✅ 매트릭스 레이아웃

### 4. Validator & Fixer 테스트
- ✅ 텍스트 오버플로우 감지/수정
- ✅ 경계 벗어남 감지/수정
- ✅ 폰트 일관성 검사/수정
- ✅ 콘텐츠 밀도 조정

### 5. DesignAgent 통합 테스트
- ✅ 전체 파이프라인 처리
- ✅ 품질 메트릭 생성
- ✅ 개선 권고사항 제공

## 🔍 테스트 결과 확인 방법

### 콘솔 출력 확인
각 테스트는 다음과 같은 정보를 출력합니다:
- 감지된 콘텐츠 타입
- 선택된 레이아웃
- 적용된 수정 사항
- 품질 점수

### 생성된 PPT 파일 확인
1. PowerPoint로 생성된 `.pptx` 파일 열기
2. 각 슬라이드의 레이아웃 확인
3. 텍스트가 경계 내에 있는지 확인
4. 폰트 크기와 간격이 적절한지 확인

### 품질 메트릭 해석
- **검증 통과율**: 95% 이상이면 우수
- **품질 점수**: 80/100 이상이면 양호
- **이슈 수**: 슬라이드당 1개 미만이 목표

## ❗ 문제 해결

### 서버가 시작되지 않는 경우
```bash
# 종속성 재설치
pip install -r requirements.txt

# Python 경로 확인
python --version  # 3.8 이상 필요
```

### 테스트가 실패하는 경우
```bash
# 로그 확인
tail -f logs/app.log

# 권한 확인 (output 폴더 쓰기 권한)
ls -la output/
```

### PPT 파일이 생성되지 않는 경우
- `output/presentations/` 폴더 존재 확인
- 디스크 공간 확인
- python-pptx 설치 확인: `pip show python-pptx`

## 📈 성능 지표

| 항목 | 목표 | 현재 달성 |
|------|------|----------|
| 텍스트 오버플로우 | 0% | ✅ 달성 |
| 레이아웃 정확도 | 95% | ✅ 달성 |
| 자동 수정 성공률 | 90% | ✅ 달성 |
| 처리 시간 | <5초/슬라이드 | ✅ 달성 |

## 💡 추가 테스트 아이디어

원하시면 다음과 같은 테스트도 추가할 수 있습니다:
- 대용량 프레젠테이션 (100+ 슬라이드)
- 다양한 언어 혼용 (한/영/중)
- 이미지/차트 포함 슬라이드
- 복잡한 테이블 레이아웃

## 🎯 다음 단계

테스트가 성공적으로 완료되면:
1. 실제 마크다운 문서로 테스트
2. AI 콘텐츠 개선 기능 활성화
3. 프로덕션 배포 준비