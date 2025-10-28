"""
한글 파일 업로드 테스트 스크립트
"""

import requests
import time
import json
from datetime import datetime

def test_korean_document():
    """한글 문서로 PPT 생성 테스트"""
    
    print("="*60)
    print("한글 문서 PPT 생성 테스트")
    print("="*60)
    
    # 짧은 한글 텍스트로 테스트 (Rate Limit 방지)
    test_document = """
    e-HR 시스템 MVP 구축 프로젝트
    
    1. 프로젝트 개요
    - 목표: 6개월 내 e-HR 시스템 MVP 구축
    - 방법: AI 코딩 도구 활용
    - 대상: 비전문가 PM
    
    2. 추진 전략
    - Phase 1: 요구사항 정의
    - Phase 2: 시스템 설계
    - Phase 3: 구현 및 테스트
    
    3. 기대 효과
    - 개발 기간 50% 단축
    - 비용 70% 절감
    - 품질 향상
    """
    
    # 1. PPT 생성 요청
    print("\n1. PPT 생성 요청 중...")
    
    ppt_request = {
        "document": test_document,
        "num_slides": 5,  # 적은 수의 슬라이드로 테스트
        "target_audience": "Executive Team"
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/generate-ppt', 
            json=ppt_request
        )
        
        if response.status_code != 200:
            print(f"[ERROR] PPT 생성 요청 실패: {response.status_code}")
            print(response.text)
            return
        
        ppt_id = response.json()['ppt_id']
        print(f"[SUCCESS] PPT ID: {ppt_id}")
        
        # 2. 상태 추적
        print("\n2. 생성 진행상태 추적...")
        print("-"*40)
        
        start_time = time.time()
        max_wait = 180  # 3분 최대 대기
        
        for i in range(max_wait):
            response = requests.get(f'http://localhost:8000/api/v1/ppt-status/{ppt_id}')
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'unknown')
                progress = data.get('progress', 0)
                stage = data.get('current_stage', 'N/A')
                
                print(f"\r[{i+1}s] Progress: {progress:3}% | Status: {status:10} | Stage: {stage:20}", end='')
                
                if status == 'completed':
                    print(f"\n\n[SUCCESS] PPT 생성 완료!")
                    print(f"  - 소요 시간: {time.time() - start_time:.1f}초")
                    print(f"  - 품질 점수: {data.get('quality_score', 'N/A')}")
                    print(f"  - 다운로드 URL: http://localhost:8000{data.get('download_url', '')}")
                    
                    # 성공 요약
                    print("\n" + "="*60)
                    print("테스트 성공!")
                    print("한글 문서로 PPT 생성이 정상 작동합니다.")
                    print("="*60)
                    return
                    
                elif status == 'failed':
                    print(f"\n\n[ERROR] 생성 실패!")
                    print(f"  - 오류: {data.get('error', 'Unknown error')}")
                    print(f"  - 상태: {data}")
                    
                    # 실패 원인 분석
                    print("\n" + "="*60)
                    print("테스트 실패 - 오류 세부사항:")
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    print("="*60)
                    return
            
            time.sleep(1)
        
        print("\n[ERROR] 시간 초과: 3분 이상 소요")
        
    except Exception as e:
        print(f"\n[ERROR] 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

def check_server():
    """서버 상태 확인"""
    try:
        response = requests.get('http://localhost:8000/api/v1/health')
        if response.status_code == 200:
            print("[OK] 서버가 정상 작동 중입니다.")
            return True
    except:
        print("[ERROR] 서버에 연결할 수 없습니다.")
        return False
    return False

if __name__ == "__main__":
    if check_server():
        test_korean_document()
    else:
        print("Docker 컨테이너를 먼저 시작해주세요:")
        print("  cd mckinsey-ppt-generator && docker-compose up -d")