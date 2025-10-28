"""
McKinsey PPT 생성 API 엔드포인트
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime
import os
from loguru import logger # Added this import

# 로컬 임포트
from app.services.workflow_engine import WorkflowEngine
from app.core.redis_client import RedisClient
from app.core.config import settings

router = APIRouter(prefix="/api/v1", tags=["PPT Generation"])

# ================================
# 데이터 모델 정의
# ================================

class PPTGenerationRequest(BaseModel):
    """PPT 생성 요청 모델"""
    document: str = Field(
        ..., 
        min_length=100,
        description="PPT로 변환할 비즈니스 문서 (최소 100자)"
    )
    style: str = Field(
        default="mckinsey",
        description="PPT 스타일 (mckinsey, modern, minimal)"
    )
    target_audience: str = Field(
        default="executive",
        description="타겟 청중 (executive, technical, general)"
    )
    num_slides: int = Field(
        default=15,
        ge=5,
        le=30,
        description="생성할 슬라이드 수 (5-30장)"
    )
    language: str = Field(
        default="ko",
        description="언어 코드 (ko, en, ja)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "document": "2024년 시장 분석 보고서...",
                "style": "mckinsey",
                "target_audience": "executive",
                "num_slides": 15,
                "language": "ko"
            }
        }

class PPTGenerationResponse(BaseModel):
    """PPT 생성 응답 모델"""
    ppt_id: str = Field(..., description="PPT 생성 작업 고유 ID")
    status: str = Field(..., description="작업 상태 (processing, completed, failed)")
    message: str = Field(..., description="상태 메시지")
    estimated_time: int = Field(..., description="예상 완료 시간 (초)")
    created_at: datetime = Field(..., description="요청 생성 시간")
    
class PPTStatusResponse(BaseModel):
    """PPT 생성 상태 응답 모델"""
    ppt_id: str
    status: str  # processing, completed, failed
    progress: int  # 0-100
    current_stage: Optional[str] = None
    current_stage_description: Optional[str] = None
    quality_score: Optional[float] = None
    download_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    estimated_completion: Optional[datetime] = None

# ================================
# API 엔드포인트
# ================================

@router.post(
    "/generate-ppt",
    response_model=PPTGenerationResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="PPT 생성 요청",
    description="비즈니스 문서를 입력받아 McKinsey 수준의 PPT 생성 작업을 시작합니다."
)
async def generate_ppt(
    request: PPTGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    PPT 생성 요청 엔드포인트
    
    작업 흐름:
    1. 고유 PPT ID 생성
    2. 초기 상태를 Redis에 저장
    3. 백그라운드 작업 큐에 추가
    4. 즉시 202 Accepted 응답 반환
    """
    try:
        # 1. 고유 PPT ID 생성
        ppt_id = str(uuid.uuid4())
        
        # 2. 초기 상태 저장
        redis_client = RedisClient()
        initial_status = {
            "ppt_id": ppt_id,
            "status": "processing",
            "progress": 0,
            "current_stage": "initializing",
            "current_stage_description": "PPT 생성 작업 초기화 중...",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "request": request.dict()
        }
        
        await redis_client.set_ppt_status(ppt_id, initial_status)
        
        # 3. 백그라운드 작업 추가
        background_tasks.add_task(
            process_ppt_generation,
            ppt_id=ppt_id,
            request_data=request.dict()
        )
        
        # 4. 응답 반환
        return PPTGenerationResponse(
            ppt_id=ppt_id,
            status="processing",
            message="PPT 생성 작업이 시작되었습니다. /ppt-status/{ppt_id}로 진행 상황을 확인하세요.",
            estimated_time=300,  # 5분 예상
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PPT 생성 요청 처리 중 오류 발생: {str(e)}"
        )

@router.get(
    "/ppt-status/{ppt_id}",
    response_model=PPTStatusResponse,
    summary="PPT 생성 상태 조회",
    description="PPT 생성 작업의 현재 진행 상황을 조회합니다."
)
async def get_ppt_status(ppt_id: str):
    """
    PPT 생성 상태 조회 엔드포인트
    
    반환 정보:
    - 현재 진행 단계 (0-100%)
    - 현재 처리 중인 에이전트
    - 품질 점수 (완료 시)
    - 다운로드 URL (완료 시)
    - 에러 메시지 (실패 시)
    """
    try:
        redis_client = RedisClient()
        status_data = await redis_client.get_ppt_status(ppt_id)
        
        if not status_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PPT ID {ppt_id}를 찾을 수 없습니다."
            )
        
        return PPTStatusResponse(**status_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"상태 조회 중 오류 발생: {str(e)}"
        )

@router.get(
    "/download/{ppt_id}",
    response_class=FileResponse,
    summary="PPT 파일 다운로드",
    description="생성 완료된 PPTX 파일을 다운로드합니다."
)
async def download_ppt(ppt_id: str):
    """
    PPT 파일 다운로드 엔드포인트
    
    전제 조건:
    - PPT 생성이 완료된 상태 (status=completed)
    - 파일이 서버에 존재
    """
    try:
        redis_client = RedisClient()
        status_data = await redis_client.get_ppt_status(ppt_id)
        
        # 1. PPT 존재 확인
        if not status_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PPT ID {ppt_id}를 찾을 수 없습니다."
            )
        
        # 2. 완료 상태 확인
        if status_data["status"] != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"PPT 생성이 아직 완료되지 않았습니다. 현재 상태: {status_data['status']}"
            )
        
        # 3. 파일 경로 확인
        file_path = status_data.get("file_path")
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PPT 파일을 찾을 수 없습니다."
            )
        
        # 4. 파일 다운로드
        return FileResponse(
            path=file_path,
            filename=f"mckinsey_presentation_{ppt_id[:8]}.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"파일 다운로드 중 오류 발생: {str(e)}"
        )

# ================================
# 백그라운드 작업 함수
# ================================

async def process_ppt_generation(ppt_id: str, request_data: dict):
    """
    백그라운드에서 실행되는 PPT 생성 프로세스
    
    작업 흐름:
    1. WorkflowEngine 초기화
    2. 5개 에이전트 순차 실행
    3. 각 단계마다 Redis 상태 업데이트
    4. PPT 데이터 생성 완료
    5. 파일 생성 (Task 6에서 구현 예정)
    6. 최종 상태 업데이트
    """
    logger.info(f"process_ppt_generation started for ppt_id: {ppt_id}") # Added this log
    redis_client = RedisClient()
    
    try:
        # 1. WorkflowEngine 초기화
        await redis_client.update_ppt_status(ppt_id, {
            "progress": 5,
            "current_stage": "workflow_init",
            "current_stage_description": "워크플로우 엔진 초기화 중..."
        })
        
        engine = WorkflowEngine()
        
        # 2. 워크플로우 실행
        result = await engine.execute(
            input_data={
                'job_id': ppt_id,
                'document': request_data["document"],
                'style': request_data["style"],
                'target_audience': request_data["target_audience"],
                'num_slides': request_data["num_slides"]
            }
        )
        
        # 3. 품질 검증
        if result["quality_score"] < 0.85:
            raise Exception(f"품질 기준 미달: {result['quality_score']}")
        
        # 4. 파일 생성
        from app.services.pptx_generator import PptxGenerator
        pptx_generator = PptxGenerator()
        file_path = pptx_generator.generate(result['ppt_data'])
        
        # 5. 완료 상태 업데이트
        await redis_client.update_ppt_status(ppt_id, {
            "status": "completed",
            "progress": 100,
            "current_stage": "completed",
            "current_stage_description": "PPT 생성 완료!",
            "quality_score": result["quality_score"],
            "file_path": file_path,
            "download_url": f"/api/v1/download/{ppt_id}",
            "updated_at": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        # 에러 발생 시 상태 업데이트
        await redis_client.update_ppt_status(ppt_id, {
            "status": "failed",
            "progress": -1,
            "current_stage": "error",
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        # 로깅
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"PPT 생성 실패 (ID: {ppt_id}): {str(e)}", exc_info=True)

async def update_progress(redis_client, ppt_id: str, stage: str, progress: int):
    """진행 상황 업데이트 헬퍼 함수"""
    stage_descriptions = {
        "strategist": "전략 구조 설계 중 (MECE + 피라미드)...",
        "data_analyst": "데이터 분석 및 인사이트 도출 중...",
        "storyteller": "스토리라인 구성 중 (SCR 구조)...",
        "designer": "McKinsey 스타일 적용 중...",
        "quality_review": "품질 검증 중 (So What 테스트)..."
    }
    
    await redis_client.update_ppt_status(ppt_id, {
        "progress": progress,
        "current_stage": stage,
        "current_stage_description": stage_descriptions.get(stage, "처리 중..."),
        "updated_at": datetime.utcnow().isoformat()
    })
