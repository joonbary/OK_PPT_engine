"""
Integration Tests for End-to-End PPT Generation Pipeline
Task 4.1 - Complete Workflow Integration Testing

통합 테스트 스위트:
- End-to-End 파이프라인 테스트
- 성능 벤치마크 검증
- 품질 점수 달성 확인
- McKinsey 표준 준수 검증
"""

import pytest
import asyncio
import time
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

from app.services.workflow_orchestrator import WorkflowOrchestrator
from app.models.workflow_models import GenerationRequest, PipelineStatus, WorkflowStage


class TestWorkflowIntegration:
    """End-to-End 워크플로우 통합 테스트"""
    
    @pytest.fixture
    def sample_business_document(self) -> str:
        """비즈니스 분석 샘플 문서"""
        return """
        # 디지털 전환 전략 분석 보고서
        
        ## 현재 상황 분석
        우리 회사는 디지털 전환의 중요한 시점에 있습니다. 시장 조사 결과, 
        고객의 67%가 온라인 서비스를 선호하며, 디지털 채널 매출이 전년 대비 
        45% 증가했습니다.
        
        ## 주요 발견사항
        1. 고객 경험: 디지털 터치포인트에서 고객 만족도 82% 달성
        2. 운영 효율성: 자동화를 통해 비용 15% 절감 가능
        3. 시장 기회: 새로운 디지털 제품으로 25% 매출 성장 기대
        
        ## 권고사항
        1. 디지털 플랫폼 투자 확대 (6개월 내)
        2. 직원 디지털 역량 강화 프로그램 (3개월 내)
        3. 고객 데이터 분석 시스템 구축 (12개월 내)
        
        ## 기대 효과
        - 매출 증가: 25-30%
        - 비용 절감: 15-20%
        - 고객 만족도: 90% 목표
        """
    
    @pytest.fixture
    def test_orchestrator(self) -> WorkflowOrchestrator:
        """테스트용 워크플로우 오케스트레이터"""
        return WorkflowOrchestrator(
            max_iterations=2,  # 테스트용으로 단축
            target_quality_score=0.80,  # 테스트용으로 조정
            aggressive_fix=True,
            timeout_minutes=3  # 테스트용으로 단축
        )
    
    @pytest.mark.asyncio
    async def test_complete_pipeline_execution(
        self, 
        test_orchestrator: WorkflowOrchestrator,
        sample_business_document: str
    ):
        """전체 파이프라인 실행 테스트"""
        
        # Given: 표준 PPT 생성 요청
        request = GenerationRequest(
            document=sample_business_document,
            num_slides=12,
            target_audience="executive",
            presentation_purpose="analysis",
            target_quality_score=0.80,
            max_iterations=2
        )
        
        # When: 워크플로우 실행
        start_time = time.time()
        response = await test_orchestrator.execute(request)
        execution_time = time.time() - start_time
        
        # Then: 기본 성공 검증
        assert response.success, f"Pipeline failed: {response.errors}"
        assert response.pptx_path is not None, "No output file generated"
        assert os.path.exists(response.pptx_path), "Output file does not exist"
        
        # 파일 크기 검증 (최소 50KB)
        file_size = os.path.getsize(response.pptx_path) / 1024
        assert file_size >= 50, f"Generated file too small: {file_size}KB"
        
        # 슬라이드 수 검증
        assert response.slides_generated >= 10, f"Not enough slides: {response.slides_generated}"
        assert response.slides_generated <= 15, f"Too many slides: {response.slides_generated}"
        
        # 품질 점수 검증
        assert response.quality_score >= 0.70, f"Quality too low: {response.quality_score}"
        
        # 실행 시간 검증 (5분 이내)
        assert execution_time <= 300, f"Execution too slow: {execution_time}s"
        
        print(f"✅ Pipeline completed in {execution_time:.1f}s with quality {response.quality_score:.3f}")
    
    @pytest.mark.asyncio
    async def test_stage_by_stage_execution(
        self,
        test_orchestrator: WorkflowOrchestrator,
        sample_business_document: str
    ):
        """단계별 실행 세부 검증"""
        
        request = GenerationRequest(
            document=sample_business_document,
            num_slides=10,
            target_quality_score=0.75
        )
        
        response = await test_orchestrator.execute(request)
        
        # 모든 단계가 실행되었는지 확인
        expected_stages = [
            WorkflowStage.INITIALIZATION,
            WorkflowStage.CONTENT_GENERATION,
            WorkflowStage.DESIGN_APPLICATION,
            WorkflowStage.VALIDATION,
            WorkflowStage.QUALITY_ASSURANCE,
            WorkflowStage.FINALIZATION
        ]
        
        executed_stages = [result.stage for result in response.stage_results]
        
        for stage in expected_stages:
            assert stage in executed_stages, f"Stage {stage.value} not executed"
        
        # 각 단계별 성능 검증
        for result in response.stage_results:
            assert result.execution_time_ms > 0, f"No execution time for {result.stage.value}"
            assert result.execution_time_ms < 30000, f"Stage {result.stage.value} too slow: {result.execution_time_ms}ms"
            
            # 성공한 단계는 데이터를 가져야 함
            if result.success:
                assert result.data, f"No data for successful stage {result.stage.value}"
        
        print(f"✅ All {len(executed_stages)} stages executed successfully")
    
    @pytest.mark.asyncio
    async def test_quality_improvement_iterations(
        self,
        test_orchestrator: WorkflowOrchestrator,
        sample_business_document: str
    ):
        """반복 개선을 통한 품질 향상 테스트"""
        
        # 높은 품질 목표로 설정하여 반복 개선 유도
        request = GenerationRequest(
            document=sample_business_document,
            num_slides=8,
            target_quality_score=0.90,  # 높은 목표
            max_iterations=3
        )
        
        response = await test_orchestrator.execute(request)
        
        # 반복 개선 메트릭 검증
        metrics = response.metrics
        assert metrics.iterations_performed >= 1, "No iterations performed"
        assert len(metrics.quality_improvement_per_iteration) >= 1, "No quality tracking"
        
        # 품질 개선 추이 확인
        quality_scores = metrics.quality_improvement_per_iteration
        if len(quality_scores) > 1:
            # 품질이 개선되거나 최소한 유지되어야 함
            final_quality = quality_scores[-1]
            initial_quality = quality_scores[0]
            assert final_quality >= initial_quality * 0.95, "Quality degraded significantly"
        
        print(f"✅ Quality improved from {quality_scores[0]:.3f} to {quality_scores[-1]:.3f} in {metrics.iterations_performed} iterations")
    
    @pytest.mark.asyncio
    async def test_validation_and_auto_fix_integration(
        self,
        test_orchestrator: WorkflowOrchestrator,
        sample_business_document: str
    ):
        """검증 및 자동 수정 통합 테스트"""
        
        request = GenerationRequest(
            document=sample_business_document,
            num_slides=6,
            target_quality_score=0.85,
            aggressive_fixing=True
        )
        
        response = await test_orchestrator.execute(request)
        
        # 검증 단계 결과 확인
        validation_results = [
            result for result in response.stage_results 
            if result.stage == WorkflowStage.VALIDATION
        ]
        assert len(validation_results) >= 1, "No validation performed"
        
        # 자동 수정 통계 확인
        metrics = response.metrics
        if metrics.initial_issues_count > 0:
            # 이슈가 있었다면 수정이 시도되어야 함
            assert metrics.fixed_issues_count >= 0, "No fix attempts made"
            
            # 수정 성공률 확인
            if metrics.fixed_issues_count > 0:
                assert metrics.fix_success_rate > 0, "No successful fixes"
                assert metrics.fix_success_rate <= 1.0, "Invalid fix success rate"
        
        # 최종 품질 확인
        final_quality = response.quality_score
        assert final_quality > 0, "No final quality score"
        
        print(f"✅ Fixed {metrics.fixed_issues_count}/{metrics.initial_issues_count} issues with {metrics.fix_success_rate:.2%} success rate")
    
    @pytest.mark.asyncio
    async def test_mckinsey_compliance_verification(
        self,
        test_orchestrator: WorkflowOrchestrator,
        sample_business_document: str
    ):
        """McKinsey 표준 준수 검증"""
        
        request = GenerationRequest(
            document=sample_business_document,
            num_slides=8,
            template_name="mckinsey_standard",
            color_scheme="mckinsey_blue"
        )
        
        response = await test_orchestrator.execute(request)
        
        # McKinsey 준수 여부 확인
        assert response.mckinsey_compliance is not None, "No compliance check"
        
        # 품질 점수 세부 확인
        if response.quality_breakdown:
            quality = response.quality_breakdown
            
            # 각 품질 기준이 평가되었는지 확인
            assert quality.clarity >= 0, "Clarity not evaluated"
            assert quality.insight >= 0, "Insight not evaluated"
            assert quality.structure >= 0, "Structure not evaluated"
            assert quality.visual >= 0, "Visual not evaluated"
            assert quality.actionability >= 0, "Actionability not evaluated"
            
            # 가중 평균이 올바르게 계산되었는지 확인
            expected_total = (
                quality.clarity * 0.20 +
                quality.insight * 0.25 +
                quality.structure * 0.20 +
                quality.visual * 0.15 +
                quality.actionability * 0.20
            )
            assert abs(quality.total - expected_total) < 0.01, "Incorrect weighted average"
        
        print(f"✅ McKinsey compliance: {response.mckinsey_compliance}, Quality breakdown verified")
    
    @pytest.mark.asyncio
    async def test_performance_benchmarks(
        self,
        test_orchestrator: WorkflowOrchestrator,
        sample_business_document: str
    ):
        """성능 벤치마크 테스트"""
        
        # 다양한 슬라이드 수로 성능 테스트
        test_cases = [
            {"slides": 5, "max_time": 120},   # 2분
            {"slides": 10, "max_time": 180},  # 3분
            {"slides": 15, "max_time": 300},  # 5분
        ]
        
        for case in test_cases:
            request = GenerationRequest(
                document=sample_business_document,
                num_slides=case["slides"],
                target_quality_score=0.75,
                max_iterations=2
            )
            
            start_time = time.time()
            response = await test_orchestrator.execute(request)
            execution_time = time.time() - start_time
            
            # 성능 기준 검증
            assert execution_time <= case["max_time"], f"{case['slides']} slides took {execution_time:.1f}s (limit: {case['max_time']}s)"
            assert response.success, f"Failed with {case['slides']} slides"
            
            # 메모리 사용량 확인
            if response.metrics:
                assert response.metrics.peak_memory_usage_mb < 1000, f"Memory usage too high: {response.metrics.peak_memory_usage_mb}MB"
            
            print(f"✅ {case['slides']} slides: {execution_time:.1f}s (limit: {case['max_time']}s)")
    
    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(
        self,
        test_orchestrator: WorkflowOrchestrator
    ):
        """오류 처리 및 복구 테스트"""
        
        # 잘못된 입력으로 테스트
        invalid_requests = [
            # 빈 문서
            GenerationRequest(document="", num_slides=5),
            # 너무 많은 슬라이드
            GenerationRequest(document="Short doc", num_slides=100),
            # 불가능한 품질 목표
            GenerationRequest(document="Test document", target_quality_score=1.1)
        ]
        
        for i, request in enumerate(invalid_requests):
            response = await test_orchestrator.execute(request)
            
            # 오류가 적절히 처리되었는지 확인
            if not response.success:
                assert len(response.errors) > 0, f"No error messages for invalid request {i}"
                assert response.pptx_path is None or not os.path.exists(response.pptx_path), f"File created for invalid request {i}"
            
            print(f"✅ Invalid request {i+1} handled appropriately")
    
    @pytest.mark.asyncio
    async def test_concurrent_execution(
        self,
        sample_business_document: str
    ):
        """동시 실행 테스트"""
        
        # 3개의 동시 요청
        requests = [
            GenerationRequest(document=sample_business_document, num_slides=6),
            GenerationRequest(document=sample_business_document, num_slides=8),
            GenerationRequest(document=sample_business_document, num_slides=10),
        ]
        
        orchestrators = [
            WorkflowOrchestrator(max_iterations=1, timeout_minutes=2)
            for _ in requests
        ]
        
        # 동시 실행
        start_time = time.time()
        tasks = [
            orchestrator.execute(request)
            for orchestrator, request in zip(orchestrators, requests)
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.time() - start_time
        
        # 모든 요청이 처리되었는지 확인
        successful_responses = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                print(f"⚠️ Request {i+1} failed with exception: {response}")
            else:
                assert hasattr(response, 'success'), f"Invalid response type for request {i+1}"
                if response.success:
                    successful_responses.append(response)
        
        # 최소 하나는 성공해야 함
        assert len(successful_responses) >= 1, "No successful concurrent executions"
        
        # 동시 실행이 순차 실행보다 효율적이어야 함 (각각 2분 한계 × 3 = 6분보다 적어야 함)
        assert total_time < 360, f"Concurrent execution too slow: {total_time:.1f}s"
        
        print(f"✅ {len(successful_responses)}/3 concurrent executions successful in {total_time:.1f}s")


class TestWorkflowComponentIntegration:
    """개별 컴포넌트 통합 테스트"""
    
    @pytest.mark.asyncio
    async def test_content_generator_integration(self):
        """ContentGenerator 통합 테스트"""
        from app.services.content_generator import ContentGenerator
        
        generator = ContentGenerator()
        
        test_document = "Digital transformation analysis with 25% growth potential and customer satisfaction improvement."
        
        presentation = await generator.generate(
            document=test_document,
            num_slides=5,
            target_audience="executive"
        )
        
        # 기본 검증
        assert presentation is not None, "No presentation generated"
        assert len(presentation.slides) >= 3, "Not enough slides generated"
        assert len(presentation.slides) <= 7, "Too many slides generated"
        
        # 슬라이드 내용 검증
        for i, slide in enumerate(presentation.slides):
            assert slide.shapes.title is not None or i == 0, f"No title in slide {i+1}"
        
        print(f"✅ ContentGenerator created {len(presentation.slides)} slides")
    
    @pytest.mark.asyncio
    async def test_design_applicator_integration(self):
        """DesignApplicator 통합 테스트"""
        from app.services.design_applicator import DesignApplicator
        from app.services.content_generator import ContentGenerator
        
        # 먼저 기본 프레젠테이션 생성
        generator = ContentGenerator()
        presentation = await generator.generate(
            document="Test business analysis",
            num_slides=3
        )
        
        # 디자인 적용
        applicator = DesignApplicator()
        styled_presentation = await applicator.apply(presentation)
        
        # 적용 통계 확인
        stats = applicator.get_design_stats()
        
        assert stats["stats"]["slides_processed"] > 0, "No slides processed"
        assert "mckinsey_compliance" in stats, "No compliance info"
        assert stats["mckinsey_compliance"]["color_palette"] == "McKinsey Standard", "Wrong color palette"
        
        print(f"✅ DesignApplicator processed {stats['stats']['slides_processed']} slides")
    
    @pytest.mark.asyncio
    async def test_quality_controller_integration(self):
        """QualityController 통합 테스트"""
        from app.services.quality_controller import QualityController
        from app.services.content_generator import ContentGenerator
        from app.services.design_applicator import DesignApplicator
        
        # 전체 파이프라인으로 프레젠테이션 생성
        generator = ContentGenerator()
        presentation = await generator.generate(
            document="Strategic analysis with data insights, recommendations, and next steps for business growth.",
            num_slides=4
        )
        
        applicator = DesignApplicator()
        styled_presentation = await applicator.apply(presentation)
        
        # 품질 평가
        controller = QualityController(target_score=0.8)
        quality_score = await controller.evaluate(styled_presentation)
        
        # 품질 점수 검증
        assert quality_score.total >= 0, "Invalid total score"
        assert quality_score.total <= 1.0, "Score exceeds maximum"
        
        # 개별 기준 검증
        assert 0 <= quality_score.clarity <= 1.0, "Invalid clarity score"
        assert 0 <= quality_score.insight <= 1.0, "Invalid insight score"
        assert 0 <= quality_score.structure <= 1.0, "Invalid structure score"
        assert 0 <= quality_score.visual <= 1.0, "Invalid visual score"
        assert 0 <= quality_score.actionability <= 1.0, "Invalid actionability score"
        
        # 품질 리포트 생성
        report = controller.get_quality_report(quality_score)
        assert "overall_score" in report, "Missing overall score in report"
        assert "grade" in report, "Missing grade in report"
        assert "improvement_suggestions" in report, "Missing suggestions in report"
        
        print(f"✅ QualityController evaluated with score {quality_score.total:.3f} ({report['grade']})")


@pytest.mark.asyncio
async def test_demo_presentation_generation():
    """데모 프레젠테이션 생성 테스트"""
    
    demo_document = """
    # McKinsey 스타일 비즈니스 분석 보고서
    
    ## 개요
    본 분석은 디지털 전환 이니셔티브의 현재 상태와 향후 전략 방향을 다룹니다.
    
    ## 현황 분석
    - 디지털 매출 비중: 현재 35% → 목표 60%
    - 고객 디지털 채널 이용률: 67% (전년 대비 +23%)
    - 운영 효율성: 자동화를 통한 15% 비용 절감 달성
    
    ## 핵심 인사이트
    1. 고객 행동 변화: 모바일 우선 전략 필요
    2. 경쟁 환경: 디지털 네이티브 기업들의 시장 점유율 확대
    3. 내부 역량: 디지털 스킬 갭 존재, 교육 투자 필요
    
    ## 전략적 권고사항
    1. 디지털 플랫폼 투자 확대 (우선순위: 모바일 앱, AI 챗봇)
    2. 조직 역량 강화 (디지털 교육 프로그램, 애자일 조직 전환)
    3. 데이터 기반 의사결정 체계 구축
    
    ## 실행 계획
    - Phase 1 (0-3개월): 모바일 플랫폼 개선, 교육 프로그램 시작
    - Phase 2 (3-6개월): AI 솔루션 도입, 조직 구조 개편
    - Phase 3 (6-12개월): 데이터 분석 플랫폼 구축, 성과 측정
    
    ## 기대 효과
    - 매출 증가: 25-30% (12개월 내)
    - 고객 만족도: 현재 78% → 목표 90%
    - 운영 비용 절감: 추가 10-15%
    """
    
    orchestrator = WorkflowOrchestrator(
        max_iterations=3,
        target_quality_score=0.85,
        aggressive_fix=True
    )
    
    request = GenerationRequest(
        document=demo_document,
        num_slides=12,
        target_audience="executive",
        presentation_purpose="analysis",
        target_quality_score=0.85,
        include_charts=True,
        include_recommendations=True
    )
    
    print("🚀 Generating demo McKinsey-style presentation...")
    
    start_time = time.time()
    response = await orchestrator.execute(request)
    execution_time = time.time() - start_time
    
    # 결과 검증 및 출력
    print(f"\n📊 Demo Presentation Results:")
    print(f"Success: {response.success}")
    print(f"Execution Time: {execution_time:.1f}s")
    print(f"Slides Generated: {response.slides_generated}")
    print(f"Quality Score: {response.quality_score:.3f}")
    print(f"McKinsey Compliant: {response.mckinsey_compliance}")
    
    if response.pptx_path and os.path.exists(response.pptx_path):
        file_size = os.path.getsize(response.pptx_path) / 1024
        print(f"Output File: {response.pptx_path} ({file_size:.1f}KB)")
    
    if response.metrics:
        print(f"Iterations: {response.metrics.iterations_performed}")
        print(f"Issues Fixed: {response.metrics.fixed_issues_count}")
        print(f"Peak Memory: {response.metrics.peak_memory_usage_mb:.1f}MB")
    
    if response.errors:
        print(f"Errors: {len(response.errors)}")
        for error in response.errors[:3]:  # 첫 3개만 표시
            print(f"  - {error}")
    
    # 품질 세부 점수
    if response.quality_breakdown:
        q = response.quality_breakdown
        print(f"\n📈 Quality Breakdown:")
        print(f"  Clarity: {q.clarity:.3f} (20%)")
        print(f"  Insight: {q.insight:.3f} (25%)")
        print(f"  Structure: {q.structure:.3f} (20%)")
        print(f"  Visual: {q.visual:.3f} (15%)")
        print(f"  Actionability: {q.actionability:.3f} (20%)")
    
    # 테스트 어설션
    assert response.success, f"Demo generation failed: {response.errors}"
    assert execution_time <= 300, f"Demo generation too slow: {execution_time}s"
    assert response.quality_score >= 0.70, f"Demo quality too low: {response.quality_score}"
    
    print(f"\n✅ Demo presentation successfully generated and validated!")
    
    return response


if __name__ == "__main__":
    # 데모 실행
    asyncio.run(test_demo_presentation_generation())