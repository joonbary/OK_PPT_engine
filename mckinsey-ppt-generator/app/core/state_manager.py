"""
단계별 실행 상태와 중간 결과를 Redis에 저장/조회하는 경량 StateManager.

본 구현은 Redis 캐시 중심으로 동작하며, DB 영속화가 필요할 경우
별도 PhaseResult 모델을 추가로 연동하도록 확장 가능하다.
"""

from __future__ import annotations

from typing import Dict, Optional
from datetime import datetime
from enum import Enum
import json

from app.core.redis_client import RedisClient


class PhaseStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class PhaseName(str, Enum):
    ANALYZE = "analyze"
    STRUCTURE = "structure"
    CONTENT = "content"
    DESIGN = "design"
    REVIEW = "review"


class StateManager:
    def __init__(self, cache_ttl: int = 3600) -> None:
        self.redis = RedisClient()
        self.cache_ttl = cache_ttl

    def _key(self, project_id: str, phase: PhaseName) -> str:
        return f"phase:{project_id}:{phase.value}"

    async def set_status(
        self,
        project_id: str,
        phase: PhaseName,
        status: PhaseStatus,
        result: Optional[Dict] = None,
        meta: Optional[Dict] = None,
    ) -> None:
        payload = {
            "project_id": project_id,
            "phase": phase.value,
            "status": status.value,
            "result": result or {},
            "meta": meta or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        await self.redis.set_ppt_status(self._key(project_id, phase), payload, ttl=self.cache_ttl)

    async def get_status(self, project_id: str, phase: PhaseName) -> Optional[Dict]:
        data = await self.redis.get_ppt_status(self._key(project_id, phase))
        return data

