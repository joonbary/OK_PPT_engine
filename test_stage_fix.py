"""
진행률 추적 stage None 문제 수정 테스트
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{BASE_URL}/api/v1/generate-ppt"
STATUS_ENDPOINT = f"{BASE_URL}/api/v1/ppt-status"

TEST_DOCUMENT = """
Test Document for Stage Tracking

1. Market Overview
- Global market size: $500B
- Growth rate: 20% annually

2. Strategy
- Target market share: 5%
- Investment: $50M
"""

def test_stage_tracking():
    """Stage 추적 테스트"""
    print("\n" + "="*60)
    print("Stage Tracking Test")
    print("="*60)
    
    # 1. PPT 생성 요청
    print("\n1. Sending PPT generation request...")
    request_data = {
        "document": TEST_DOCUMENT,
        "num_slides": 5,
        "target_audience": "Executive Board"
    }
    
    response = requests.post(API_ENDPOINT, json=request_data)
    if response.status_code != 200:
        print(f"[ERROR] Request failed: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    ppt_id = response.json().get("ppt_id")
    print(f"[SUCCESS] PPT ID: {ppt_id}")
    
    # 2. Stage 추적
    print("\n2. Tracking stages...")
    stages_seen = []
    last_stage = None
    none_count = 0
    
    for i in range(100):  # 최대 100초
        response = requests.get(f"{STATUS_ENDPOINT}/{ppt_id}")
        if response.status_code == 200:
            data = response.json()
            current_stage = data.get("current_stage")
            progress = data.get("progress", 0)
            status = data.get("status")
            
            # Stage 변경 감지
            if current_stage != last_stage:
                timestamp = datetime.now().strftime('%H:%M:%S')
                
                if current_stage is None:
                    none_count += 1
                    print(f"[{timestamp}] [WARNING] Stage: None (count: {none_count}) | Progress: {progress}% | Status: {status}")
                else:
                    print(f"[{timestamp}] [OK] Stage: {current_stage} | Progress: {progress}% | Status: {status}")
                    if current_stage not in stages_seen:
                        stages_seen.append(current_stage)
                
                last_stage = current_stage
            
            # 완료 확인
            if status in ["completed", "failed"]:
                print(f"\n[{status.upper()}] Final stage: {current_stage}")
                print(f"Full data: {json.dumps(data, indent=2)}")
                break
        
        time.sleep(1)
    
    # 3. 결과 분석
    print("\n" + "="*60)
    print("Test Results")
    print("="*60)
    
    print(f"\nStages observed: {len(stages_seen)}")
    for i, stage in enumerate(stages_seen, 1):
        print(f"  {i}. {stage}")
    
    print(f"\nNone occurrences: {none_count}")
    
    if none_count == 0:
        print("\n[SUCCESS] No 'None' stages detected!")
        print("The issue has been fixed.")
    else:
        print(f"\n[WARNING] Detected {none_count} 'None' stage(s)")
        print("The issue may still exist.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    test_stage_tracking()