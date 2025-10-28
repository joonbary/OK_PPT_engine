"""
AI 헤드라인 PPT 반영 테스트 스크립트
"""

import requests
import json
import time
import asyncio
from datetime import datetime

# 테스트 서버 설정
BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{BASE_URL}/api/v1/generate-ppt"
STATUS_ENDPOINT = f"{BASE_URL}/api/v1/ppt-status"

# 테스트 문서 콘텐츠
TEST_DOCUMENT = """
글로벌 전기차 시장 진출 전략 분석

1. 시장 현황
- 2025년 글로벌 전기차 시장: 8,500억 달러 규모 (전년 대비 18% 성장)
- 아시아 시장 비중: 전체의 42% (3,570억 달러)
- 우리 회사 현재 위치: 시장 점유율 1.2% (연매출 102억 달러)

2. 경쟁 환경 분석
- 주요 경쟁사: Tesla 25%, BYD 18%, Volkswagen 12%
- 우리 핵심 강점: 배터리 기술 업계 1위, 충전 속도 경쟁사 대비 30% 빠름
- 개선 필요: 브랜드 인지도 경쟁사 대비 50% 낮은 수준

3. 성장 기회 포착
- 정부 보조금: 2026년까지 30% 증액 예정
- 충전 인프라: 향후 3년간 2배 확대 투자 계획
- 중산층 확대: 구매력 있는 소비자층 25% 증가 전망

4. 전략 목표 설정
- 3개년 목표: 시장 점유율 3.5% 달성 (현재 1.2% → 목표 3.5%, 2.9배 증가)
- 목표 매출: 300억 달러 (3배 성장)
- 투자 규모: 총 150억 달러 (R&D 60억 + 마케팅 40억 + 생산설비 50억)
- 기대 수익: ROI 180% (5년 누적 기준)

5. 실행 로드맵
- Phase 1 (6개월): 주요 5개국 시장 심층 조사 및 현지 파트너십 구축
- Phase 2 (1년): 플래그십 전기차 모델 2종 시장 출시
- Phase 3 (2년): 생산 능력 3배 확대 및 판매 네트워크 전국 구축
- Phase 4 (3년): 프리미엄 라인 진출 및 자율주행 Level 4 기능 탑재

6. 리스크 관리 전략
- 원자재 가격 변동: 선물 헤지 전략으로 15% 가격 리스크 완화
- 규제 변화 대응: 각국 정책 전담 모니터링 팀 운영
- 기술 경쟁 심화: 연간 R&D 투자 20% 증액으로 기술 격차 유지
"""


def test_ppt_generation():
    """PPT 생성 테스트 실행"""
    print(f"\n{'='*60}")
    print(f"AI Headline PPT Test Started")
    print(f"{'='*60}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. PPT 생성 요청
    print("\nStep 1: Sending PPT generation request...")
    request_data = {
        "document": TEST_DOCUMENT,
        "num_slides": 6,
        "target_audience": "Executive Board"
    }
    
    try:
        response = requests.post(API_ENDPOINT, json=request_data)
        if response.status_code == 200:
            result = response.json()
            ppt_id = result.get("ppt_id")
            print(f"[SUCCESS] PPT generation request successful!")
            print(f"   PPT ID: {ppt_id}")
            return ppt_id
        else:
            print(f"[ERROR] PPT generation request failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        return None


def track_ppt_status(ppt_id):
    """PPT 생성 상태 추적"""
    print(f"\nStep 2: Tracking PPT generation status...")
    print(f"   PPT ID: {ppt_id}")
    
    start_time = time.time()
    stages_timeline = []
    last_stage = None
    last_progress = 0
    
    while True:
        try:
            response = requests.get(f"{STATUS_ENDPOINT}/{ppt_id}")
            if response.status_code == 200:
                data = response.json()
                elapsed = time.time() - start_time
                
                # 진행률 표시
                progress = data.get("progress", 0)
                stage = data.get("current_stage", "")
                status = data.get("status", "")
                
                # 단계 변경 감지
                if stage != last_stage or progress != last_progress:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    
                    if stage != last_stage:
                        stages_timeline.append({
                            "stage": stage,
                            "progress": progress,
                            "time": timestamp,
                            "elapsed": f"{elapsed:.1f}s"
                        })
                        print(f"\n   [NEW STAGE] [{timestamp}] {stage}")
                    
                    # 프로그레스 바
                    bar_length = 30
                    filled = int(bar_length * progress / 100)
                    bar = '#' * filled + '-' * (bar_length - filled)
                    
                    print(f"   [{bar}] {progress}% | {stage} | {elapsed:.1f}s", end='\r')
                    
                    last_stage = stage
                    last_progress = progress
                
                # 완료 처리
                if status == "completed":
                    print(f"\n\n{'='*60}")
                    print(f"[COMPLETED] PPT generation complete!")
                    print(f"{'='*60}")
                    print(f"Total Time: {elapsed:.1f} seconds")
                    print(f"Quality Score: {data.get('quality_score', 'N/A')}")
                    print(f"Download URL: {data.get('download_url', 'N/A')}")
                    
                    print(f"\nStage Timeline:")
                    for i, stage_info in enumerate(stages_timeline, 1):
                        print(f"   {i}. {stage_info['stage'].ljust(20)} | {str(stage_info['progress']).rjust(3)}% | {stage_info['time']} (+{stage_info['elapsed']})")
                    
                    return {
                        "success": True,
                        "quality_score": data.get("quality_score"),
                        "download_url": data.get("download_url"),
                        "elapsed_time": elapsed,
                        "stages": stages_timeline
                    }
                
                # 실패 처리
                if status == "failed":
                    print(f"\n[FAILED] PPT generation failed!")
                    print(f"   Error: {data.get('error', 'Unknown error')}")
                    return {
                        "success": False,
                        "error": data.get("error")
                    }
                    
            time.sleep(1)
            
            # 타임아웃 (5분)
            if elapsed > 300:
                print(f"\n[WARNING] Timeout: exceeded 5 minutes")
                return {"success": False, "error": "Timeout"}
                
        except Exception as e:
            print(f"\n[ERROR] Status check failed: {e}")
            return {"success": False, "error": str(e)}


def verify_ai_headlines():
    """AI headline verification"""
    print(f"\n{'='*60}")
    print(f"Step 3: AI Headline Verification")
    print(f"{'='*60}")
    
    expected_headlines = [
        "Global EV market offers maximum growth with 180% ROI in 3 years",
        "Asia market reaches 42% share with $357B scale",
        "Battery tech and charging speed secure 30% advantage over competitors",
        "Market share target to increase 2.9x from 1.2% to 3.5%",
        "$15B investment over 5 years enables 180% ROI"
    ]
    
    print("\nExpected AI Headlines:")
    for i, headline in enumerate(expected_headlines, 2):
        print(f"   Slide {i}: {headline}")
    
    print("\nVerification Checklist:")
    print("   [ ] Detailed sentences of 15+ characters")
    print("   [ ] Quantitative numbers included (%, dollars, multiples)")
    print("   [ ] Strategic action verbs used")
    print("   [ ] Input document content accurately reflected")
    print("   [ ] McKinsey style compliance")


def main():
    """Main test execution"""
    # 1. PPT generation request
    ppt_id = test_ppt_generation()
    
    if not ppt_id:
        print("\n[ERROR] Test aborted: PPT generation request failed")
        return
    
    # 2. 상태 추적
    result = track_ppt_status(ppt_id)
    
    # 3. AI 헤드라인 검증
    verify_ai_headlines()
    
    # 4. Final results
    print(f"\n{'='*60}")
    print(f"Test Results Summary")
    print(f"{'='*60}")
    
    if result.get("success"):
        print(f"[SUCCESS] Test completed successfully!")
        print(f"   - PPT ID: {ppt_id}")
        print(f"   - Quality Score: {result.get('quality_score', 'N/A')}")
        print(f"   - Elapsed Time: {result.get('elapsed_time', 0):.1f} seconds")
        print(f"   - Download: http://localhost:8000{result.get('download_url', '')}")
        
        # Quality score evaluation
        quality_score = result.get("quality_score", 0)
        if quality_score and float(quality_score) >= 0.85:
            print(f"   [ACHIEVED] Target quality score (0.85) reached!")
        else:
            print(f"   [WARNING] Quality score needs improvement (target: 0.85)")
    else:
        print(f"[FAILED] Test failed!")
        print(f"   - Error: {result.get('error', 'Unknown error')}")
    
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()