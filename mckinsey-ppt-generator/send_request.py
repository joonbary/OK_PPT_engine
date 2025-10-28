import requests
import json
import time

# 긴 테스트 문서 (Pydantic 유효성 검사 통과용)
test_document = """
아시아 시장 진출 전략 분석

1. 시장 개요
- 아시아 시장 규모: 5조원
- 연평균 성장률: 15%
- 주요 국가: 베트남, 인도네시아, 태국

2. 기회 요인
- 중산층 급증: 5년 내 2배 성장 예상
- 디지털 전환 가속화
- 정부 지원 정책 강화

3. 진출 전략
- 1단계: 베트남 시장 선점 (향후 6개월)
- 2단계: 인도네시아 확장 (12개월 후)
- 3단계: 지역 허브 구축 (18개월 후)

4. 예상 효과
- 매출 30% 증가
- 시장 점유율 15% 달성
- ROI 150% 달성
"""

payload = {
    "document": test_document,
    "style": "mckinsey",
    "target_audience": "executive",
    "num_slides": 5,
    "language": "ko"
}

print("Sending request to API...")
print(f"Document length: {len(test_document)} chars")

try:
    response = requests.post(
        "http://localhost:8000/api/v1/generate-ppt",
        json=payload,
        timeout=60
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        result = response.json()
        ppt_id = result.get("ppt_id")
        print(f"\nPPT ID: {ppt_id}")
        print("\nWaiting for generation to complete...")
        
        # 상태 확인 (최대 60초)
        for i in range(60):
            time.sleep(1)
            status_response = requests.get(f"http://localhost:8000/api/v1/ppt-status/{ppt_id}")
            status = status_response.json()
            
            print(f"[{i+1}s] Status: {status.get('status')} | Progress: {status.get('progress', 0)}%")
            
            if status.get('status') == 'completed':
                print("\nPPT generation completed!")
                print(f"Quality Score: {status.get('quality_score')}")
                print(f"Download URL: {status.get('download_url')}")
                break
            elif status.get('status') == 'failed':
                print(f"\nGeneration failed: {status.get('error')}")
                break
                
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")