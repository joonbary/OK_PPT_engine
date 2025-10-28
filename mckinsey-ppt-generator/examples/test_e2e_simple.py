
"""
End-to-End Test: Simple Document
"""


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import os
from app.services.workflow_engine import WorkflowEngine
from app.services.pptx_generator import PptxGeneratorService

async def test_simple_document():
    """
    간단한 비즈니스 문서로 PPT 생성 테스트
    """
    
    print("=" * 60)
    print("E2E 테스트 시작: 간단한 비즈니스 문서")
    print("=" * 60)
    
    # 테스트 문서
    document = """
    ## 2024년 1분기 매출 분석 보고서
    
    ### 핵심 요약
    - 1분기 매출: 1,000억원 (전년 대비 +20%)
    - 신제품 매출 기여도: 60%
    - 아시아 시장 성장률: 35%
    
    ### 주요 발견사항
    1. 신제품 라인이 예상을 초과하는 성과를 보임
    2. 아시아 시장에서 경쟁사 대비 2배 빠른 성장
    3. 디지털 채널 매출이 전체의 45% 차지
    
    ### 전략적 시사점
    - 신제품 투자 확대 필요
    - 아시아 시장 진출 가속화
    - 디지털 역량 강화 요구
    
    ### 권고사항
    1. 신제품 생산 능력 30% 증설
    2. 아시아 3개 신규 거점 설립
    3. 디지털 마케팅 예산 50% 증액
    """
    
    try:
        # 1. 워크플로우 실행
        print("[1/3] 워크플로우 실행 중...")
        print("- Strategist: MECE 구조 설계")
        print("- DataAnalyst: 데이터 분석 및 인사이트")
        print("- Storyteller: SCR 스토리라인 구성")
        print("- Designer: McKinsey 스타일 적용")
        print("- QualityReview: 품질 검증")
        
        engine = WorkflowEngine()
        result = await engine.execute(
            input_data={
                'job_id': 'e2e_simple',
                'document': document,
                'style': "mckinsey",
                'target_audience': "executive",
                'num_slides': 10
            }
        )
        
        if result['status'] == 'completed':
            print("[OK] 워크플로우 완료!")
            print(f"   품질 점수: {result['quality_score']:.3f}")
            # num_slides is now in metadata
            num_slides = result['metadata']['num_slides']
            print(f"   생성된 슬라이드: {num_slides}장")

            # PPTX 파일 경로는 WorkflowEngine에서 이미 생성되어 반환됨
            file_path = result['pptx_file_path']
            
            # 2. 파일 검증
            print("[2/3] 파일 검증 중...") # Changed step number

            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print("[OK] PPTX 파일 경로 확인!")
            print(f"   파일 경로: {file_path}")
            print(f"   파일 크기: {file_size_mb:.2f} MB")

            assert os.path.exists(file_path), "파일이 생성되지 않음"
            assert file_path.endswith(".pptx"), "PPTX 확장자 아님"
            assert file_size_mb > 0.01, "파일 크기가 너무 작음"

            print("[OK] 파일 검증 통과!")

            # 최종 결과
            print("=" * 60)
            print("E2E 테스트 성공!")
            print("=" * 60)
            print(f"파일 위치: {file_path}")
            print("PowerPoint로 열어서 확인하세요!")
            print(f"   - 슬라이드 수: {num_slides}장")
            print(f"   - 품질 점수: {result['quality_score']:.3f}")
            print(f"   - McKinsey 스타일 적용됨")

            return {
                "success": True,
                "file_path": file_path,
                "quality_score": result['quality_score'],
                "num_slides": num_slides
            }
        else:
            print(f"[FAIL] 워크플로우 실패: {result.get('error')}")
            return {"success": False, "error": result.get('error')}

    except Exception as e:
        print(f"[FAIL] E2E 테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    result = asyncio.run(test_simple_document())
    
    if result["success"]:
        print("[OK] 모든 테스트 통과!")
    else:
        print(f"[FAIL] 테스트 실패: {result['error']}")
