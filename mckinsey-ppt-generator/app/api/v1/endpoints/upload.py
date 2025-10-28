"""
파일 업로드 엔드포인트
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from typing import Dict
import uuid

from app.services.document_parser import DocumentParser
from app.core.config import settings

router = APIRouter()

# 업로드 디렉토리 설정
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...)
) -> Dict:
    """
    문서 파일 업로드 및 텍스트 추출
    
    지원 형식: DOCX, PDF, MD
    최대 크기: 10MB
    
    Returns:
        {
            "success": true,
            "text": "추출된 텍스트...",
            "filename": "example.docx",
            "file_size": 2345678,
            "format": "docx"
        }
    """
    
    # 파일 형식 검증
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in DocumentParser.SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(DocumentParser.SUPPORTED_FORMATS)}"
        )
    
    # 임시 파일로 저장
    file_id = str(uuid.uuid4())
    temp_path = UPLOAD_DIR / f"{file_id}{file_ext}"
    
    try:
        # 파일 저장
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 파일 크기 확인
        file_size = temp_path.stat().st_size
        if file_size > DocumentParser.MAX_FILE_SIZE:
            temp_path.unlink()  # 파일 삭제
            raise HTTPException(
                status_code=400,
                detail=f"파일 크기가 너무 큽니다 (최대 10MB, 현재: {file_size / 1024 / 1024:.2f}MB)"
            )
        
        # 텍스트 추출
        extracted_text = DocumentParser.parse_file(str(temp_path))
        
        # 임시 파일 삭제
        temp_path.unlink()
        
        return {
            "success": True,
            "text": extracted_text,
            "filename": file.filename,
            "file_size": file_size,
            "format": file_ext[1:]  # '.docx' -> 'docx'
        }
        
    except Exception as e:
        # 에러 발생 시 임시 파일 삭제
        if temp_path.exists():
            temp_path.unlink()
        
        raise HTTPException(
            status_code=500,
            detail=f"파일 처리 중 오류 발생: {str(e)}"
        )


@router.get("/supported-formats")
async def get_supported_formats() -> Dict:
    """
    지원하는 파일 형식 목록 반환
    """
    return {
        "formats": DocumentParser.SUPPORTED_FORMATS,
        "max_size_mb": DocumentParser.MAX_FILE_SIZE / (1024 * 1024),
        "descriptions": {
            ".docx": "Microsoft Word 문서",
            ".pdf": "PDF 문서",
            ".md": "Markdown 문서"
        }
    }