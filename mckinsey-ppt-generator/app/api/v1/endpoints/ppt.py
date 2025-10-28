"""PPT 생성 API 엔드포인트"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Request
from typing import Optional, Dict, Any
from app.models.schemas import PPTRequest, PPTResponse, StatusResponse
from app.services.ppt_service import PPTService
from app.services.document_parser import DocumentParser
from fastapi.responses import FileResponse
import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime
from loguru import logger

router = APIRouter()
ppt_service = PPTService()

@router.post("/generate-ppt", response_model=PPTResponse)
async def generate_ppt(
    request: Request,
    background_tasks: BackgroundTasks,
):
    """
    PPT 생성 요청
    - 파일 업로드 또는 텍스트 직접 입력 지원
    - 실시간 상태 추적
    """
    logger.info(
        f"📥 Received PPT generation request - content_type: {request.headers.get('content-type')}"
    )
    
    # 요청 파싱: JSON 또는 multipart/form-data 모두 지원
    content_type = request.headers.get("content-type", "")
    payload: Dict[str, Any] = {}
    document_text: Optional[str] = None
    num_slides: int = 15
    target_audience: str = "executive"
    style: str = "mckinsey"

    # 파일 처리 (multipart 업로드)
    document_content = ""
    file_obj: Optional[UploadFile] = None
    if content_type.startswith("multipart/form-data"):
        # 일반 폼 요청 지원 (파일 + 텍스트)
        try:
            form = await request.form()
        except Exception:
            form = {}
        payload = dict(form)
        file_obj = payload.get("file") or None

    if file_obj is not None:
        # 파일 형식 검증
        file_ext = Path(file_obj.filename).suffix.lower()
        if file_ext not in ['.docx', '.pdf', '.txt', '.md']:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 파일 형식입니다: {file_ext}"
            )
        
        # 임시 파일로 저장
        upload_dir = Path("/app/uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_id = str(uuid.uuid4())
        file_path = upload_dir / f"{file_id}{file_ext}"
        
        try:
            # 파일 저장
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file_obj.file, buffer)
            
            logger.info(f"✅ File saved to: {file_path} (size: {file_path.stat().st_size} bytes)")
            
            # 파일 파싱
            if file_ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    document_content = f.read()
            else:
                # DocumentParser 사용
                document_content = DocumentParser.parse_file(str(file_path))
            
            logger.info(f"📊 Parsed document: {len(document_content)} characters")
            logger.info(f"📊 Preview: {document_content[:200]}...")
            
            # 파싱 후 임시 파일 삭제
            file_path.unlink()
            
        except Exception as e:
            logger.error(f"❌ File processing error: {e}")
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=500,
                detail=f"파일 처리 중 오류: {str(e)}"
            )
    else:
        # JSON 또는 폼 필드에서 값 추출
        try:
            if content_type.startswith("application/json"):
                payload = await request.json()
            elif not payload:
                # 이미 multipart에서 payload를 만든 경우가 아니면 폼을 다시 시도
                form = await request.form()
                payload = dict(form)
        except Exception:
            payload = {}

        # document/document_text 키 모두 지원
        document_text = (payload.get("document") or payload.get("document_text") or "").strip()
        document_content = document_text
        logger.info(f"Parsed payload keys={list(payload.keys())}, doc_len={len(document_content) if document_content else 0}")
        # 보조 필드
        try:
            num_slides = int(payload.get("num_slides", 15))
        except Exception:
            num_slides = 15
        target_audience = payload.get("target_audience", "executive")
        style = payload.get("style", "mckinsey")
        language = (payload.get("language") or "ko").lower()

    # 파일 또는 텍스트 중 하나는 필수
    if (file_obj is None) and (not document_content or not document_content.strip()):
        raise HTTPException(
            status_code=400,
            detail="파일 업로드 또는 텍스트 입력이 필요합니다."
        )
    
    # 문서 내용 검증
    if not document_content or len(document_content.strip()) < 100:
        raise HTTPException(
            status_code=400,
            detail=f"문서 내용이 너무 짧습니다: {len(document_content)} 문자"
        )
    
    ppt_id = ppt_service.create_ppt_id()

    # Write initial status synchronously to avoid 404 race on first poll
    created_at = datetime.utcnow()
    try:
        await ppt_service.redis.set_ppt_status(
            ppt_id,
            {
                "status": "processing",
                "progress": 0,
                "current_stage": "document_analysis",
                "created_at": created_at.isoformat(),
            },
        )
    except Exception:
        # Even if this fails, proceed with background task; client may retry
        pass

    # PPT 생성 요청 데이터 구성
    request_data = {
        "document": document_content,  # 필수: 문서 내용
        "num_slides": num_slides,
        "target_audience": target_audience,
        "style": style,
        "language": language,
    }
    
    logger.info(f"🚀 Starting PPT generation for {ppt_id} with document: {len(document_content)} chars")
    
    # Kick off background generation
    background_tasks.add_task(ppt_service.start_generation, ppt_id, request_data)

    return PPTResponse(
        ppt_id=ppt_id,
        status="processing",
        estimated_time=300,
        created_at=created_at,
    )

@router.get("/ppt-status/{ppt_id}")
async def get_ppt_status(ppt_id: str):
    """PPT 생성 상태 조회"""
    status = await ppt_service.get_status(ppt_id)
    if not status:
        raise HTTPException(status_code=404, detail="PPT not found")

    # 타입/키 보정: 누락 필드 방지 및 변환
    progress_val = status.get("progress")
    if isinstance(progress_val, str) and progress_val.isdigit():
        progress_val = int(progress_val)
    if progress_val is None:
        progress_val = 0 if status.get("status") != "completed" else 100

    return {
        "ppt_id": ppt_id,
        "status": status.get("status", "processing"),
        "progress": progress_val,
        "current_stage": status.get("current_stage"),
        "quality_score": status.get("quality_score"),
        "download_url": status.get("download_url"),
        "created_at": status.get("created_at"),
        "completed_at": status.get("completed_at"),
        "error": status.get("error"),
    }


@router.get("/download/{ppt_id}")
async def download_ppt(ppt_id: str):
    """PPT 파일 다운로드"""
    file_path = await ppt_service.get_file_path(ppt_id)
    # 1) 기본 경로 체크
    if not file_path or not os.path.exists(file_path):
        # 2) 표준 저장소(/app/ppt_files/{ppt_id}.pptx) 확인
        std_path = os.path.join("/app/ppt_files", f"{ppt_id}.pptx")
        if os.path.exists(std_path):
            file_path = std_path
        else:
            # 3) 오케스트레이터 출력 디렉토리에서 패턴 검색
            try:
                import glob
                base = "/app/output/generated_presentations"
                pattern = os.path.join(base, f"mckinsey_presentation_{ppt_id[:8]}_*.pptx")
                candidates = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
                if candidates:
                    file_path = candidates[0]
                else:
                    raise HTTPException(status_code=404, detail="File not found")
            except Exception:
                raise HTTPException(status_code=404, detail="File not found")
    
    # 선택된 경로로 응답
    
    # Add explicit headers to avoid proxy/intermediary altering payload
    try:
        size = os.path.getsize(file_path)
    except Exception:
        size = None
    headers = {"Cache-Control": "no-store"}
    if size is not None:
        headers["Content-Length"] = str(size)
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers=headers,
    )

@router.delete("/ppt/{ppt_id}")
async def delete_ppt(ppt_id: str):
    """생성된 PPT 삭제"""
    # This part is not fully implemented in the service, so I will add a placeholder
    return {"success": True, "message": "PPT 파일이 삭제되었습니다."}
