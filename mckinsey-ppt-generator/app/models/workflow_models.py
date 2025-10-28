"""
Workflow Models for End-to-End PPT Generation Pipeline
Task 4.1 - Complete Content Generation Workflow Integration
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


class WorkflowStage(Enum):
    """워크플로우 실행 단계"""
    INITIALIZATION = "initialization"
    CONTENT_GENERATION = "content_generation"
    DESIGN_APPLICATION = "design_application"
    VALIDATION = "validation"
    AUTO_FIX = "auto_fix"
    QUALITY_ASSURANCE = "quality_assurance"
    FINALIZATION = "finalization"


class PipelineStatus(Enum):
    """파이프라인 실행 상태"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class StageResult:
    """개별 단계 실행 결과"""
    stage: WorkflowStage
    success: bool
    data: Dict[str, Any]
    metrics: Dict[str, float]
    issues: List[str] = field(default_factory=list)
    execution_time_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    stage_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class PipelineMetrics:
    """파이프라인 전체 성능 메트릭"""
    total_execution_time_ms: float = 0.0
    content_generation_time_ms: float = 0.0
    design_application_time_ms: float = 0.0
    validation_time_ms: float = 0.0
    auto_fix_time_ms: float = 0.0
    quality_assurance_time_ms: float = 0.0
    finalization_time_ms: float = 0.0
    
    # 품질 메트릭
    initial_issues_count: int = 0
    fixed_issues_count: int = 0
    remaining_issues_count: int = 0
    fix_success_rate: float = 0.0
    final_quality_score: float = 0.0
    
    # 반복 메트릭
    iterations_performed: int = 0
    quality_improvement_per_iteration: List[float] = field(default_factory=list)
    
    # 리소스 사용량
    peak_memory_usage_mb: float = 0.0
    slides_generated: int = 0
    tokens_used: int = 0


@dataclass
class QualityScore:
    """품질 평가 점수"""
    clarity: float = 0.0        # 명확성 (20%)
    insight: float = 0.0        # 인사이트 (25%)  
    structure: float = 0.0      # 구조 (20%)
    visual: float = 0.0         # 시각적 품질 (15%)
    actionability: float = 0.0  # 실행가능성 (20%)
    total: float = 0.0          # 가중 평균
    passed: bool = False        # 목표 달성 여부
    target_score: float = 0.85  # 목표 점수
    
    def calculate_total(self, weights: Optional[Dict[str, float]] = None) -> float:
        """가중 평균 계산"""
        if weights is None:
            weights = {
                "clarity": 0.20,
                "insight": 0.25,
                "structure": 0.20,
                "visual": 0.15,
                "actionability": 0.20
            }
        
        self.total = (
            self.clarity * weights["clarity"] +
            self.insight * weights["insight"] +
            self.structure * weights["structure"] +
            self.visual * weights["visual"] +
            self.actionability * weights["actionability"]
        )
        
        self.passed = self.total >= self.target_score
        return self.total


@dataclass
class SlideGenerationSpec:
    """개별 슬라이드 생성 명세"""
    slide_number: int
    title: str
    content_type: str  # "text", "chart", "image", "table", "mixed"
    content: Dict[str, Any]
    layout_type: str = "content_with_caption"
    priority: int = 1  # 1=high, 2=medium, 3=low
    estimated_complexity: float = 0.5  # 0.0-1.0
    
    # 시각화 요구사항
    chart_requirements: Optional[Dict[str, Any]] = None
    image_requirements: Optional[Dict[str, Any]] = None
    
    # 품질 요구사항
    min_quality_score: float = 0.8
    must_pass_validation: bool = True


@dataclass
class ContentGenerationContext:
    """콘텐츠 생성 컨텍스트"""
    document: str
    target_audience: str = "executive"
    presentation_purpose: str = "analysis"
    num_slides: int = 15
    time_limit_minutes: int = 5
    
    # 스타일 요구사항
    color_scheme: str = "mckinsey_standard"
    font_preferences: List[str] = field(default_factory=lambda: ["Arial", "Calibri"])
    layout_preferences: List[str] = field(default_factory=list)
    
    # 콘텐츠 요구사항
    include_executive_summary: bool = True
    include_recommendations: bool = True
    max_bullets_per_slide: int = 5
    prefer_visuals: bool = True
    
    # 품질 요구사항
    target_quality_score: float = 0.85
    max_iterations: int = 3
    aggressive_fixing: bool = True


@dataclass
class WorkflowContext:
    """워크플로우 실행 컨텍스트"""
    workflow_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    request: ContentGenerationContext = field(default_factory=ContentGenerationContext)
    stage_results: List[StageResult] = field(default_factory=list)
    current_iteration: int = 0
    status: PipelineStatus = PipelineStatus.PENDING
    
    # 실행 상태
    current_stage: Optional[WorkflowStage] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # 결과 데이터
    presentation = None  # pptx.Presentation 객체
    output_path: Optional[str] = None
    
    # 메트릭 및 품질
    metrics: PipelineMetrics = field(default_factory=PipelineMetrics)
    quality_scores: List[QualityScore] = field(default_factory=list)
    
    # 오류 및 로깅
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def add_stage_result(self, result: StageResult):
        """단계 결과 추가 및 메트릭 업데이트"""
        self.stage_results.append(result)
        
        # 실행 시간 메트릭 업데이트
        if result.stage == WorkflowStage.CONTENT_GENERATION:
            self.metrics.content_generation_time_ms = result.execution_time_ms
        elif result.stage == WorkflowStage.DESIGN_APPLICATION:
            self.metrics.design_application_time_ms = result.execution_time_ms
        elif result.stage == WorkflowStage.VALIDATION:
            self.metrics.validation_time_ms = result.execution_time_ms
        elif result.stage == WorkflowStage.AUTO_FIX:
            self.metrics.auto_fix_time_ms = result.execution_time_ms
        elif result.stage == WorkflowStage.QUALITY_ASSURANCE:
            self.metrics.quality_assurance_time_ms = result.execution_time_ms
        elif result.stage == WorkflowStage.FINALIZATION:
            self.metrics.finalization_time_ms = result.execution_time_ms
    
    def get_latest_quality_score(self) -> Optional[QualityScore]:
        """최신 품질 점수 반환"""
        return self.quality_scores[-1] if self.quality_scores else None
    
    def calculate_total_execution_time(self) -> float:
        """총 실행 시간 계산 (ms)"""
        if self.started_at and self.completed_at:
            # started_at과 completed_at이 float(timestamp)인 경우
            if isinstance(self.started_at, (int, float)) and isinstance(self.completed_at, (int, float)):
                return (self.completed_at - self.started_at) * 1000
            # datetime 객체인 경우
            elif hasattr(self.started_at, 'total_seconds') and hasattr(self.completed_at, 'total_seconds'):
                delta = self.completed_at - self.started_at
                return delta.total_seconds() * 1000
        return 0.0
    
    def get_stage_result(self, stage: WorkflowStage) -> Optional[StageResult]:
        """특정 단계의 결과 반환"""
        for result in reversed(self.stage_results):  # 최신 결과부터 검색
            if result.stage == stage:
                return result
        return None
    
    def has_critical_errors(self) -> bool:
        """치명적 오류 존재 여부 확인"""
        return any("critical" in error.lower() for error in self.errors)
    
    def get_success_rate(self) -> float:
        """전체 단계 성공률 계산"""
        if not self.stage_results:
            return 0.0
        
        successful_stages = sum(1 for result in self.stage_results if result.success)
        return successful_stages / len(self.stage_results)


@dataclass 
class GenerationRequest:
    """PPT 생성 요청"""
    document: str
    num_slides: int = 15
    target_audience: str = "executive"
    presentation_purpose: str = "analysis"
    output_format: str = "pptx"
    
    # 품질 요구사항
    target_quality_score: float = 0.85
    max_iterations: int = 3
    aggressive_fixing: bool = True
    
    # 스타일 요구사항
    template_name: str = "mckinsey_standard"
    color_scheme: str = "mckinsey_blue"
    
    # 시간 제한
    max_execution_time_minutes: int = 5
    
    # 고급 옵션
    include_charts: bool = True
    include_recommendations: bool = True
    custom_instructions: Optional[str] = None
    
    def to_context(self) -> ContentGenerationContext:
        """GenerationRequest를 ContentGenerationContext로 변환"""
        return ContentGenerationContext(
            document=self.document,
            target_audience=self.target_audience,
            presentation_purpose=self.presentation_purpose,
            num_slides=self.num_slides,
            time_limit_minutes=self.max_execution_time_minutes,
            target_quality_score=self.target_quality_score,
            max_iterations=self.max_iterations,
            aggressive_fixing=self.aggressive_fixing,
            include_recommendations=self.include_recommendations
        )


@dataclass
class GenerationResponse:
    """PPT 생성 응답"""
    success: bool
    workflow_id: str
    
    # 결과 파일
    pptx_path: Optional[str] = None
    
    # 품질 메트릭
    quality_score: float = 0.0
    quality_breakdown: Optional[QualityScore] = None
    
    # 슬라이드별 결과
    slides_generated: int = 0
    slides_with_issues: int = 0
    slides_fixed: int = 0
    
    # 실행 메트릭
    total_execution_time_ms: float = 0.0
    iterations_performed: int = 0
    
    # 상세 메트릭
    metrics: Optional[PipelineMetrics] = None
    stage_results: List[StageResult] = field(default_factory=list)
    
    # 오류 및 경고
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # 추가 정보
    created_at: datetime = field(default_factory=datetime.now)
    mckinsey_compliance: bool = False
    
    @classmethod
    def from_context(cls, context: WorkflowContext) -> 'GenerationResponse':
        """WorkflowContext에서 GenerationResponse 생성"""
        latest_quality = context.get_latest_quality_score()
        
        return cls(
            success=context.status == PipelineStatus.COMPLETED,
            workflow_id=context.workflow_id,
            pptx_path=context.output_path,
            quality_score=latest_quality.total if latest_quality else 0.0,
            quality_breakdown=latest_quality,
            slides_generated=context.metrics.slides_generated,
            slides_with_issues=context.metrics.initial_issues_count,
            slides_fixed=context.metrics.fixed_issues_count,
            total_execution_time_ms=context.calculate_total_execution_time(),
            iterations_performed=context.metrics.iterations_performed,
            metrics=context.metrics,
            stage_results=context.stage_results,
            errors=context.errors,
            warnings=context.warnings,
            mckinsey_compliance=latest_quality.passed if latest_quality else False
        )