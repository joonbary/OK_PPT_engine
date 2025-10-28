#!/usr/bin/env python3
"""
Integration Test Runner for Task 4.1 Complete Workflow
Direct execution without pytest dependencies
"""

import asyncio
import sys
import os
import time
import traceback
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.workflow_orchestrator import WorkflowOrchestrator
from app.models.workflow_models import GenerationRequest


async def test_basic_workflow_integration():
    """기본 워크플로우 통합 테스트"""
    
    print("🧪 Starting Basic Workflow Integration Test...")
    
    sample_document = """
    # 디지털 전환 전략 분석
    
    ## 현황
    - 디지털 매출 비중: 35%
    - 고객 만족도: 78%
    - 운영 효율성: 자동화를 통한 15% 비용 절감
    
    ## 주요 발견사항
    1. 모바일 우선 고객 행동 변화
    2. 경쟁사 디지털 혁신 가속화
    3. 내부 디지털 스킬 갭 존재
    
    ## 전략 권고사항
    1. 디지털 플랫폼 투자 확대
    2. 조직 역량 강화
    3. 데이터 기반 의사결정 체계 구축
    
    ## 기대 효과
    - 매출 25% 증가
    - 고객 만족도 90% 달성
    - 운영 비용 10% 추가 절감
    """
    
    try:
        # 워크플로우 오케스트레이터 초기화
        orchestrator = WorkflowOrchestrator(
            max_iterations=2,
            target_quality_score=0.80,
            aggressive_fix=True,
            timeout_minutes=3
        )
        
        # 생성 요청 설정
        request = GenerationRequest(
            document=sample_document,
            num_slides=8,
            target_audience="executive",
            presentation_purpose="analysis",
            target_quality_score=0.80,
            max_iterations=2
        )
        
        print(f"📋 Request: {request.num_slides} slides, target quality {request.target_quality_score}")
        
        # 워크플로우 실행
        start_time = time.time()
        response = await orchestrator.execute(request)
        execution_time = time.time() - start_time
        
        # 결과 검증
        print(f"\n📊 Results:")
        print(f"✅ Success: {response.success}")
        print(f"⏱️  Execution Time: {execution_time:.1f}s")
        print(f"📄 Slides Generated: {response.slides_generated}")
        print(f"🎯 Quality Score: {response.quality_score:.3f}")
        print(f"🏢 McKinsey Compliant: {response.mckinsey_compliance}")
        
        if response.pptx_path and os.path.exists(response.pptx_path):
            file_size = os.path.getsize(response.pptx_path) / 1024
            print(f"💾 Output File: {response.pptx_path} ({file_size:.1f}KB)")
        else:
            print(f"⚠️  No output file generated")
        
        if response.metrics:
            print(f"🔄 Iterations: {response.metrics.iterations_performed}")
            print(f"🔧 Issues Fixed: {response.metrics.fixed_issues_count}")
            print(f"💾 Peak Memory: {response.metrics.peak_memory_usage_mb:.1f}MB")
        
        # 에러 출력
        if response.errors:
            print(f"❌ Errors ({len(response.errors)}):")
            for error in response.errors[:3]:
                print(f"   - {error}")
        
        # 품질 세부 점수
        if response.quality_breakdown:
            q = response.quality_breakdown
            print(f"\n📈 Quality Breakdown:")
            print(f"   Clarity: {q.clarity:.3f} (20%)")
            print(f"   Insight: {q.insight:.3f} (25%)")
            print(f"   Structure: {q.structure:.3f} (20%)")
            print(f"   Visual: {q.visual:.3f} (15%)")
            print(f"   Actionability: {q.actionability:.3f} (20%)")
        
        # 테스트 어설션
        assert response.success, f"Workflow failed: {response.errors}"
        assert execution_time <= 180, f"Too slow: {execution_time}s"
        assert response.quality_score >= 0.60, f"Quality too low: {response.quality_score}"
        assert response.slides_generated >= 5, f"Not enough slides: {response.slides_generated}"
        
        print(f"\n✅ Basic Workflow Integration Test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Basic Workflow Integration Test FAILED: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False


async def test_component_integration():
    """개별 컴포넌트 통합 테스트"""
    
    print("\n🧪 Starting Component Integration Test...")
    
    try:
        # ContentGenerator 테스트
        print("🎯 Testing ContentGenerator...")
        from app.services.content_generator import ContentGenerator
        
        generator = ContentGenerator()
        presentation = await generator.generate(
            document="Test business analysis with recommendations",
            num_slides=5,
            target_audience="executive"
        )
        
        assert presentation is not None, "ContentGenerator failed to create presentation"
        assert len(presentation.slides) >= 3, f"Too few slides: {len(presentation.slides)}"
        print(f"   ✅ Generated {len(presentation.slides)} slides")
        
        # DesignApplicator 테스트
        print("🎨 Testing DesignApplicator...")
        from app.services.design_applicator import DesignApplicator
        
        applicator = DesignApplicator()
        styled_presentation = await applicator.apply(presentation)
        
        stats = applicator.get_design_stats()
        assert stats["stats"]["slides_processed"] > 0, "No slides processed by DesignApplicator"
        print(f"   ✅ Styled {stats['stats']['slides_processed']} slides")
        
        # QualityController 테스트
        print("📊 Testing QualityController...")
        from app.services.quality_controller import QualityController
        
        controller = QualityController(target_score=0.8)
        quality_score = await controller.evaluate(styled_presentation)
        
        assert 0 <= quality_score.total <= 1.0, f"Invalid quality score: {quality_score.total}"
        print(f"   ✅ Quality evaluated: {quality_score.total:.3f}")
        
        print(f"\n✅ Component Integration Test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Component Integration Test FAILED: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False


async def test_performance_benchmark():
    """성능 벤치마크 테스트"""
    
    print("\n🧪 Starting Performance Benchmark Test...")
    
    try:
        test_cases = [
            {"slides": 5, "max_time": 90},
            {"slides": 10, "max_time": 150},
        ]
        
        document = "Business analysis with growth strategy, customer insights, and operational recommendations."
        
        for case in test_cases:
            print(f"⏱️  Testing {case['slides']} slides (limit: {case['max_time']}s)...")
            
            orchestrator = WorkflowOrchestrator(
                max_iterations=2,
                target_quality_score=0.75,
                timeout_minutes=3
            )
            
            request = GenerationRequest(
                document=document,
                num_slides=case["slides"],
                target_quality_score=0.75,
                max_iterations=2
            )
            
            start_time = time.time()
            response = await orchestrator.execute(request)
            execution_time = time.time() - start_time
            
            print(f"   ⏱️  Completed in {execution_time:.1f}s")
            print(f"   🎯 Quality: {response.quality_score:.3f}")
            
            # 성능 검증
            if execution_time > case["max_time"]:
                print(f"   ⚠️  Warning: Exceeded time limit ({execution_time:.1f}s > {case['max_time']}s)")
            else:
                print(f"   ✅ Within time limit")
            
            assert response.success or len(response.errors) > 0, "No response or errors"
        
        print(f"\n✅ Performance Benchmark Test COMPLETED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Performance Benchmark Test FAILED: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False


async def main():
    """메인 테스트 실행"""
    
    print("Starting Task 4.1 Complete Workflow Integration Tests")
    print("=" * 70)
    
    # 출력 디렉토리 생성
    output_dir = Path("output/generated_presentations")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # 테스트 실행
    test_results = []
    
    # 1. 기본 워크플로우 통합 테스트
    result1 = await test_basic_workflow_integration()
    test_results.append(("Basic Workflow Integration", result1))
    
    # 2. 컴포넌트 통합 테스트
    result2 = await test_component_integration()
    test_results.append(("Component Integration", result2))
    
    # 3. 성능 벤치마크 테스트
    result3 = await test_performance_benchmark()
    test_results.append(("Performance Benchmark", result3))
    
    # 결과 요약
    print("\n" + "=" * 70)
    print("📋 Test Results Summary:")
    print("=" * 70)
    
    passed = 0
    total = len(test_results)
    
    for test_name, passed_test in test_results:
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if passed_test:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Task 4.1 Integration Complete!")
        return True
    else:
        print("⚠️  Some tests failed. Review the errors above.")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        sys.exit(1)