# 🔧 한글 파일 업로드 오류 해결 보고서

## 문제 상황
- **증상**: 웹 UI에서 한글 파일 업로드 후 PPT 생성 실패
- **오류 메시지**: `status: 'failed', quality_score: 0`

## 근본 원인 분석

### 1. Claude API Rate Limit 초과 (Error 429)
- **원인**: 한글 텍스트의 많은 토큰 사용으로 인한 API 제한 초과
- **메시지**: "maximum usage increase rate for input tokens per minute"

### 2. JSON 파싱 오류
- **원인**: Storyteller Agent에서 response가 이미 dict인데 json.loads() 시도
- **메시지**: "the JSON object must be str, bytes or bytearray, not dict"

## 적용된 해결 방안

### Solution 1: GPT-4 모델로 전환
```python
# strategist_agent.py
model="gpt-4-turbo"  # Claude에서 변경
```

### Solution 2: Rate Limiter 구현
- `app/core/rate_limiter.py` 추가
- Token bucket algorithm 기반 API 호출 제한
- Claude: 5 requests/min, 5000 tokens/min
- OpenAI: 20 requests/min, 40000 tokens/min

### Solution 3: JSON 파싱 오류 수정
```python
# storyteller_agent.py
if isinstance(response, dict):
    return response  # 이미 dict면 그대로 반환
```

## 수정된 파일
1. `app/agents/strategist_agent.py` - Claude → GPT-4
2. `app/core/rate_limiter.py` - 새로 추가
3. `app/core/llm_client.py` - Rate Limiter 통합
4. `app/agents/storyteller_agent.py` - JSON 파싱 수정

## 테스트 결과
- Rate Limit 오류 해결됨
- JSON 파싱 오류 수정됨
- 짧은 한글 텍스트로 테스트 시 생성 진행

## 권장사항
1. **API 키 검증**: OpenAI API 키가 유효한지 확인
2. **토큰 사용량 모니터링**: 대용량 문서 처리 시 주의
3. **점진적 테스트**: 짧은 문서부터 시작하여 점진적으로 증가

## 현재 상태
✅ Rate Limit 문제 해결
✅ JSON 파싱 오류 수정
✅ 모델 전환 완료 (GPT-4)
⏳ 최종 테스트 진행 중

---
**작성일**: 2025-10-20
**문제 해결**: 진행 중