import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from app.services.workflow_orchestrator import WorkflowOrchestrator
from app.models.workflow_models import GenerationRequest, GenerationResponse # Corrected import

async def main():
    """
    실제 비즈니스 문서로 E2E 테스트
    """
    
    # 실제 비즈니스 문서
    document = """
    ### 2024년 사업 성과 및 2025년 전략 방향
    
    ## 주요 성과
    우리 회사의 2024년 매출은 1,200억원으로 전년 대비 25% 성장했습니다.
    이는 업계 평균 성장률 8% 대비 3배 이상 빠른 속도입니다.
    
    성장의 주요 동인:
    - 신제품 출시: 전체 매출의 65% 기여
    - 해외 매출: 전년 대비 40% 증가
    - 디지털 채널: 온라인 매출 60% 증가
    
    ## 시장 현황
    국내 시장 점유율은 35%로 업계 1위를 유지하고 있으며,
    경쟁사 대비 2배 높은 고객 만족도(92점)를 기록했습니다.
    
    해외 시장에서는 아시아 지역이 전년 대비 50% 성장하며
    최대 성장 동력으로 부상했습니다.
    
    ## 2025년 전략 방향
    
    1. 신제품 라인 확대
       - R&D 투자 50% 증액 (200억 → 300억원)
       - 신제품 5종 출시 계획
       - 목표: 신제품 매출 비중 80% 달성
    
    2. 해외 시장 공략 강화
       - 동남아 3개국 추가 진출
       - 현지 파트너십 강화
       - 목표: 해외 매출 비중 40% 달성
    
    3. 디지털 전환 가속화
       - AI 기반 개인화 추천 시스템 도입
       - 모바일 앱 리뉴얼
       - 목표: 온라인 매출 비중 50% 달성
    
    4. 운영 효율화
       - 공급망 최적화로 비용 15% 절감
       - 자동화 투자 확대
       - 목표: 영업이익률 20% 달성
    
    ## 예상 효과
    이러한 전략 실행 시 2025년 매출 1,800억원(50% 성장),
    영업이익 360억원(영업이익률 20%)을 달성할 것으로 예상됩니다.
    """
    
    # 요청 생성
    request = GenerationRequest(
        document=document,
        num_slides=12,
        target_audience="executive",
        template_name="mckinsey_standard", # Changed from style
        # language="ko" # Removed, not in GenerationRequest
    )
    
    print("=" * 60)
    print("McKinsey 수준 PPT 생성 시작...")
    print("=" * 60)
    
    # 워크플로우 실행
    orchestrator = WorkflowOrchestrator(
        max_iterations=3,
        target_quality_score=0.85,
        aggressive_fix=True
    )
    
    response = await orchestrator.execute(request)
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("생성 완료!")
    print("=" * 60)
    
    print(f"\n 성공 여부: {response.success}")
    print(f" 품질 점수: {response.quality_score:.3f} {'PASS' if response.quality_score >= 0.85 else 'WARN'}")
    print(f" 슬라이드 수: {response.slides_generated}") # Changed from response.slides
    print(f"  생성 시간: {response.total_execution_time_ms / 1000:.1f}초") # Changed from response.generation_time
    
    print(f"\n 세부 품질 점수:")
    details = response.quality_breakdown # Changed from response.quality_details
    if details: # Check if details exist
        print(f"  - 명확성 (Clarity): {details.clarity:.3f}") # Access attributes directly
        print(f"  - 인사이트 (Insight): {details.insight:.3f}")
        print(f"  - 구조 (Structure): {details.structure:.3f}")
        print(f"  - 시각 (Visual): {details.visual:.3f}")
        print(f"  - 실행가능성 (Actionability): {details.actionability:.3f}")
    else:
        print("  - 세부 품질 점수를 가져올 수 없습니다.")
    
    if response.quality_score >= 0.85:
        print("\n 목표 품질 점수 0.85 달성!")
    else:
        print(f"\n 목표 미달 (부족: {0.85 - response.quality_score:.3f})")
        print("\n개선 필요 영역:")
        if details: # Check if details exist
            # Iterate over the defined criteria in QualityScore
            criteria_scores = {
                'clarity': details.clarity,
                'insight': details.insight,
                'structure': details.structure,
                'visual': details.visual,
                'actionability': details.actionability
            }
            for criterion, score in criteria_scores.items():
                if score < 0.80:
                    print(f"  - {criterion}: {score:.3f}")
        else:
            print("  - 세부 품질 점수를 가져올 수 없어 개선 필요 영역을 표시할 수 없습니다.")
    
    print(f"\n 파일 저장: {response.pptx_path}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())