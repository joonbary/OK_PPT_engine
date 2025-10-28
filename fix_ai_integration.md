# AI 콘텐츠 통합 문제 해결 방안

## 문제 분석

### 현재 상황
1. **두 개의 워크플로우 시스템이 존재**:
   - `WorkflowEngine`: AI 에이전트를 사용하는 실제 워크플로우
   - `WorkflowOrchestrator`: ContentGenerator로 Mock PPT를 생성하는 워크플로우

2. **실제 실행 경로**:
   ```
   PPTService.start_generation()
   → WorkflowOrchestrator.execute()  # Mock 워크플로우
   → ContentGenerator.generate()      # Mock 콘텐츠 생성
   → Presentation 저장
   ```

3. **AI 워크플로우가 무시되는 이유**:
   - PPTService가 WorkflowOrchestrator만 호출
   - WorkflowEngine은 사용되지 않음

## 해결 방안

### Option 1: WorkflowOrchestrator를 WorkflowEngine으로 교체 ⭐ (권장)
PPTService가 WorkflowEngine을 직접 사용하도록 수정

**장점**:
- AI 에이전트가 실제로 작동
- 기존 AI 코드 활용
- 빠른 해결

**수정 필요 파일**:
- `app/services/ppt_service.py`

### Option 2: WorkflowOrchestrator가 WorkflowEngine을 호출
WorkflowOrchestrator의 content_generation 단계에서 WorkflowEngine 사용

**장점**:
- 기존 구조 유지
- 점진적 마이그레이션 가능

**수정 필요 파일**:
- `app/services/workflow_orchestrator.py`

### Option 3: ContentGenerator가 AI 에이전트 사용
ContentGenerator 내부에서 AI 에이전트 호출

**장점**:
- 최소한의 변경

**단점**:
- 복잡한 구조
- 중복 코드

## 추천 구현: Option 1

### 수정 코드

```python
# app/services/ppt_service.py

from app.services.workflow_engine import WorkflowEngine  # 변경
# from app.services.workflow_orchestrator import WorkflowOrchestrator  # 제거

class PPTService:
    def __init__(self):
        self.redis = RedisClient()
        self.workflow = WorkflowEngine()  # 변경
    
    async def start_generation(self, ppt_id: str, request: dict):
        try:
            # 상태를 processing으로 설정
            created_at = datetime.now().isoformat()
            await self.redis.set_ppt_status(
                ppt_id, 
                {"status": "processing", "progress": 0, "current_stage": "document_analysis", "created_at": created_at}
            )
            
            # WorkflowEngine 실행
            result = await self.workflow.execute({
                'job_id': ppt_id,
                'document': request["document"],
                'num_slides': request["num_slides"],
                'target_audience': request["target_audience"],
                'style': 'mckinsey'
            })
            
            # 결과 처리
            success = result.get('status') == 'completed'
            quality_score = result.get('quality_score', 0.0)
            pptx_path = result.get('generated_pptx_path', '')
            
            # 상태 업데이트
            await self.redis.set_ppt_status(
                ppt_id, 
                {
                    "status": "completed" if success else "failed",
                    "progress": 100,
                    "current_stage": "completed" if success else "failed",
                    "quality_score": quality_score,
                    "file_path": pptx_path,
                    "download_url": f"/api/v1/download/{ppt_id}",
                    "created_at": created_at,
                    "completed_at": datetime.now().isoformat(),
                    "error": None if success else "Generation failed"
                }
            )
            
        except Exception as e:
            await self.redis.set_ppt_status(
                ppt_id, 
                {"status": "failed", "current_stage": "failed", "error": str(e), "created_at": datetime.now().isoformat()}
            )
```

## 테스트 계획

1. 코드 수정
2. Docker 재빌드
3. 테스트 실행:
   ```bash
   python test_word_upload.py
   ```

4. 검증:
   - AI 헤드라인이 실제로 나타나는지 확인
   - 품질 점수 0.85 이상 달성
   - 입력 문서 내용이 반영되는지 확인

## 예상 결과

수정 후:
- AI 에이전트가 실제로 문서를 분석
- 5개 에이전트가 협업하여 PPT 생성
- 입력 문서의 내용이 PPT에 반영됨
- Mock 콘텐츠가 아닌 실제 AI 생성 콘텐츠