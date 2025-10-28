# -*- coding: utf-8 -*-
"""PPT 서비스: 실제 AI 워크플로우 오케스트레이션 연동"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from loguru import logger

from app.core.redis_client import RedisClient
from app.models.workflow_models import GenerationRequest
from app.services.workflow_orchestrator import WorkflowOrchestrator


class PPTService:
    def __init__(self) -> None:
        self.redis = RedisClient()
        self.orchestrator = WorkflowOrchestrator()

    def create_ppt_id(self) -> str:
        return str(uuid.uuid4())

    async def start_generation(self, ppt_id: str, request_data: Dict[str, Any]) -> None:
        """AI 파이프라인을 실행하여 실제 PPT를 생성하고 상태를 갱신한다."""
        existing = await self.redis.get_ppt_status(ppt_id) or {}
        created_at = existing.get("created_at", datetime.utcnow().isoformat())

        try:
            # 초기 상태
            await self.redis.update_ppt_status(
                ppt_id,
                {
                    "status": "processing",
                    "progress": 5,
                    "current_stage": "document_analysis",
                    "created_at": created_at,
                },
            )

            # 오케스트레이터 실행 전 중간 업데이트
            await self.redis.update_ppt_status(
                ppt_id,
                {"status": "processing", "progress": 20, "current_stage": "content_generation"},
            )

            # 요청 변환 및 실행
            req = GenerationRequest(
                document=(request_data.get("document") or "").strip(),
                num_slides=int(request_data.get("num_slides", 15)),
                target_audience=str(request_data.get("target_audience", "executive")),
            )
            # Language-aware orchestrator instance per job
            lang = (request_data.get("language") or "ko").lower()
            orchestrator = WorkflowOrchestrator(language=lang)
            result = await orchestrator.execute(req, job_id=ppt_id)

            # 진행 업데이트: 디자인/검증 구간 완료로 가정
            await self.redis.update_ppt_status(
                ppt_id,
                {"status": "processing", "progress": 80, "current_stage": "design_application"},
            )

            success = bool(getattr(result, "success", False))
            pptx_path = getattr(result, "pptx_path", None) or getattr(result, "pptx_path", None)
            quality_score = float(getattr(result, "quality_score", 0.0) or 0.0)

            if not success or not pptx_path:
                raise RuntimeError("AI pipeline failed to generate PPTX")

            # Ensure source file exists (handle async flush/IO delays)
            from pathlib import Path
            src_path = Path(pptx_path)
            if not src_path.is_absolute():
                src_path = Path("/app") / src_path
            # Poll for up to 15 seconds for file to appear
            for _ in range(150):
                if src_path.exists():
                    break
                await asyncio.sleep(0.1)
            if not src_path.exists():
                # Fallback: search by job prefix under expected folder
                try:
                    import glob
                    base = Path("/app/output/generated_presentations")
                    pattern = str(base / f"mckinsey_presentation_{ppt_id[:8]}_*.pptx")
                    candidates = sorted(glob.glob(pattern), key=lambda p: Path(p).stat().st_mtime, reverse=True)
                    if candidates:
                        src_path = Path(candidates[0])
                    else:
                        # Wider search across /app just in case
                        pattern2 = str(Path("/app") / f"**/mckinsey_presentation_{ppt_id[:8]}_*.pptx")
                        candidates = sorted(glob.glob(pattern2, recursive=True), key=lambda p: Path(p).stat().st_mtime, reverse=True)
                        if candidates:
                            src_path = Path(candidates[0])
                except Exception:
                    pass
            if not src_path.exists():
                raise RuntimeError(f"PPTX not found after generation: {src_path}")

            # 표준 다운로드 경로로 복사하여 일관성 확보 (/app/ppt_files/{ppt_id}.pptx)
            try:
                from shutil import copyfile
                dest_dir = Path("/app/ppt_files")
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_path = dest_dir / f"{ppt_id}.pptx"
                copyfile(str(src_path), str(dest_path))
                persisted_path = str(dest_path)
            except Exception as copy_err:
                logger.error(f"Failed to persist PPT to /app/ppt_files: {copy_err}")
                persisted_path = str(pptx_path)

            # 최종 상태 저장
            final_status = {
                "status": "completed",
                "progress": 100,
                "current_stage": "completed",
                "quality_score": quality_score,
                "file_path": persisted_path,
                "download_url": f"/api/v1/download/{ppt_id}",
                "created_at": created_at,
                "completed_at": datetime.utcnow().isoformat(),
                "error": None,
            }
            await self.redis.set_ppt_status(ppt_id, final_status)
            logger.info(f"✅ AI pipeline completed for {ppt_id}, saved to {pptx_path}")

        except Exception as e:
            logger.exception(f"PPT generation failed for {ppt_id}: {e}")
            await self.redis.set_ppt_status(
                ppt_id,
                {
                    "status": "failed",
                    "current_stage": "failed",
                    "progress": 100,
                    "error": str(e),
                    "created_at": created_at,
                    "completed_at": datetime.utcnow().isoformat(),
                },
            )

    async def get_status(self, ppt_id: str) -> Optional[dict]:
        return await self.redis.get_ppt_status(ppt_id)

    async def get_file_path(self, ppt_id: str) -> Optional[str]:
        status = await self.redis.get_ppt_status(ppt_id)
        if status and status.get("status") == "completed":
            return status.get("file_path")
        return None
