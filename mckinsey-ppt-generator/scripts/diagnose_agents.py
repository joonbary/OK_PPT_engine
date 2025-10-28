"""Agent 효율성 진단 스크립트"""
import asyncio
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.workflow_models import GenerationRequest
from app.services.workflow_orchestrator import WorkflowOrchestrator
from loguru import logger

async def diagnose_agents():
    """각 Agent 출력 상세 분석"""
    
    test_document = """
    전기차 시장 분석 보고서
    
    1. 시장 개요
    글로벌 전기차 시장은 2024년 기준 1,200억 달러 규모로 성장했습니다.
    전년 대비 35% 증가하며 빠른 성장세를 보이고 있습니다.
    
    2. 주요 플레이어
    - 테슬라: 시장 점유율 23%, 매출 960억 달러
    - BYD: 중국 시장 18%, 전년 대비 45% 성장
    - 현대/기아: 유럽 시장 12%, 전기차 라인업 확대 중
    
    3. 기술 동향
    - 배터리 가격: kWh당 $132 (전년 대비 15% 하락)
    - 충전 속도: 80% 충전 18분 (350kW 초급속 충전)
    - 주행거리: 평균 480km (2021년 대비 30% 증가)
    
    4. 시장 전망
    2027년까지 연평균 28% 성장 예상
    배터리 혁신과 정부 지원이 핵심 동력
    """
    
    orchestrator = WorkflowOrchestrator()
    
    print("\n" + "="*80)
    print("AGENT DIAGNOSIS - Detailed Output Analysis")
    print("="*80 + "\n")
    
    try:
        # GenerationRequest 객체 생성
        request = GenerationRequest(
            document=test_document,
            num_slides=8,
            target_audience="executive",
            presentation_purpose="strategic",  # presentation_type -> presentation_purpose
            target_quality_score=0.85
        )
        
        # WorkflowOrchestrator 실행
        result = await orchestrator.execute(request, job_id="test_diagnosis")
        
        # 결과를 dict로 변환
        result_dict = result.dict() if hasattr(result, 'dict') else result
        
        # 1. 워크플로우 상태 분석
        print("\n[1] WORKFLOW STATUS")
        print("-" * 80)
        print(f"Status: {result_dict.get('status', 'UNKNOWN')}")
        print(f"Execution time: {result_dict.get('execution_time_ms', 0):.1f}ms")
        print(f"Output path: {result_dict.get('output_path', 'NONE')}")
        
        # 2. Stage Results 분석
        print("\n[2] STAGE RESULTS")
        print("-" * 80)
        stages = result_dict.get('stage_results', [])
        for stage in stages:
            stage_name = stage.get('stage', 'UNKNOWN')
            success = stage.get('success', False)
            exec_time = stage.get('execution_time_ms', 0)
            status = "[PASS]" if success else "[FAIL]"
            print(f"  {status} {stage_name}: {exec_time:.1f}ms")
            
            # Stage별 데이터 크기 확인
            data = stage.get('data', {})
            if data:
                data_size = len(json.dumps(data))
                print(f"       Data size: {data_size} bytes")
        
        # 3. Content Generation Stage 상세 분석
        print("\n[3] CONTENT GENERATION ANALYSIS")
        print("-" * 80)
        content_stage = next((s for s in stages if 'CONTENT_GENERATION' in s.get('stage', '')), None)
        if content_stage:
            data = content_stage.get('data', {})
            print(f"Slides generated: {data.get('slides_generated', 0)}")
            print(f"Presentation created: {data.get('presentation_created', False)}")
            print(f"Content type: {data.get('content_type', 'UNKNOWN')}")
            print(f"Generation time: {data.get('generation_time', 0):.2f}s")
            print(f"Document used: {data.get('document_used', False)}")
        else:
            print("[WARNING] Content generation stage not found")
        
        # 4. Design Application Stage 분석
        print("\n[4] DESIGN APPLICATION ANALYSIS")
        print("-" * 80)
        design_stage = next((s for s in stages if 'DESIGN_APPLICATION' in s.get('stage', '')), None)
        if design_stage:
            data = design_stage.get('data', {})
            print(f"Design applied: {data.get('design_applied', False)}")
            print(f"Charts generated: {len(data.get('chart_images', []))}")
            print(f"Fonts standardized: {data.get('fonts_standardized', False)}")
            print(f"Colors applied: {data.get('colors_applied', False)}")
        else:
            print("[WARNING] Design application stage not found")
        
        # 5. Quality Assessment
        print("\n[5] QUALITY ASSESSMENT")
        print("-" * 80)
        quality_stage = next((s for s in stages if 'QUALITY_ASSURANCE' in s.get('stage', '')), None)
        if quality_stage:
            data = quality_stage.get('data', {})
            quality_score = data.get('quality_score', 0)
            passed = data.get('passed', False)
            remaining_issues = data.get('remaining_issues', 0)
            
            status = "[PASS]" if passed else "[FAIL]"
            print(f"{status} Quality Score: {quality_score:.3f}")
            print(f"Target Score: {data.get('target_score', 0.85)}")
            print(f"Remaining Issues: {remaining_issues}")
            print(f"McKinsey Compliant: {data.get('mckinsey_compliant', False)}")
        else:
            print("[WARNING] Quality assessment stage not found")
        
        # 6. Metrics Summary
        print("\n[6] PERFORMANCE METRICS")
        print("-" * 80)
        metrics = result_dict.get('metrics', {})
        print(f"Total execution time: {metrics.get('total_execution_time_ms', 0):.1f}ms")
        print(f"Slides generated: {metrics.get('slides_generated', 0)}")
        print(f"Initial issues: {metrics.get('initial_issues_count', 0)}")
        print(f"Fixed issues: {metrics.get('fixed_issues_count', 0)}")
        print(f"Final quality score: {metrics.get('final_quality_score', 0):.3f}")
        print(f"Peak memory usage: {metrics.get('peak_memory_usage_mb', 0):.1f}MB")
        
        # 7. 문제 진단
        print("\n[7] DIAGNOSIS")
        print("-" * 80)
        
        issues = []
        
        # Quality score 확인
        final_score = metrics.get('final_quality_score', 0)
        if final_score < 0.85:
            issues.append(f"[FAIL] Quality score {final_score:.3f} below target 0.85")
        
        # Content generation 확인
        if not content_stage or not content_stage.get('success'):
            issues.append("[FAIL] Content generation failed or incomplete")
        
        # Design application 확인
        if design_stage:
            charts = len(design_stage.get('data', {}).get('chart_images', []))
            if charts < 3:
                issues.append(f"[WARNING] Only {charts} charts generated (expected 3+)")
        
        # Execution time 확인
        exec_time = metrics.get('total_execution_time_ms', 0)
        if exec_time < 5000:  # 5초 미만이면 의심
            issues.append(f"[WARNING] Suspiciously fast execution: {exec_time:.1f}ms")
        
        if issues:
            print("\nISSUES FOUND:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("\n[PASS] No major issues detected")
        
        # 8. Recommendations
        print("\n[8] RECOMMENDATIONS")
        print("-" * 80)
        
        if final_score < 0.85:
            print("  1. Increase content depth and quality")
            print("  2. Add more data-driven insights")
        
        if charts < 3:
            print("  3. Generate more charts for data visualization")
        
        if exec_time < 5000:
            print("  4. Verify AI generation is actually being used (not mock data)")
        
        print("\n" + "="*80)
        print("DIAGNOSIS COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"\n[ERROR] during diagnosis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(diagnose_agents())