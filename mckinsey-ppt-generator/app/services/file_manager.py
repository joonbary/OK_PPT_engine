"""
파일 관리자
PPTX 파일 저장 및 경로 관리를 담당합니다.
"""

import os
from app.core.config import settings
from pathlib import Path
from loguru import logger

class FileManager:
    """
    파일 저장 및 관리를 위한 유틸리티 클래스
    """
    
    def __init__(self):
        self.storage_path = Path(settings.PPT_STORAGE_PATH)
        # 저장 경로가 없으면 생성
        self.storage_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"File storage initialized at: {self.storage_path}")

    def get_storage_path(self) -> Path:
        """저장 경로 반환"""
        return self.storage_path

    def save_file(self, filename: str, content: bytes) -> Path:
        """
        파일을 저장합니다.

        Args:
            filename: 저장할 파일 이름
            content: 파일 내용 (bytes)
        
        Returns:
            Path: 저장된 파일의 전체 경로
        """
        if not filename.endswith(".pptx"):
            filename += ".pptx"
            
        file_path = self.storage_path / filename
        
        try:
            with open(file_path, "wb") as f:
                f.write(content)
            logger.info(f"Successfully saved file to {file_path}")
            return file_path
        except IOError as e:
            logger.error(f"Failed to save file {file_path}: {e}")
            raise

    def get_file_path(self, filename: str) -> Path:
        """파일 경로 조회"""
        return self.storage_path / filename

    def cleanup_temp_files(self, directory: str):
        """임시 파일 정리"""
        for item in Path(directory).glob("temp_*.png"):
            try:
                item.unlink()
                logger.debug(f"Removed temp file: {item}")
            except OSError as e:
                logger.warning(f"Error removing temp file {item}: {e}")
