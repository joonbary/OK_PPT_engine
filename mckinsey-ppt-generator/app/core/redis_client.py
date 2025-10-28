"""Redis 클라이언트"""
import redis
import json
from typing import Optional

class RedisClient:
    def __init__(self):
        self.redis = redis.Redis(
            host='redis',
            port=6379,
            decode_responses=True
        )
    
    async def close(self):
        """호환용 종료 메서드(블로킹 클라이언트 닫기)."""
        try:
            self.redis.close()
        except Exception:
            pass
    
    async def set_ppt_status(self, ppt_id: str, data: dict, ttl: int = 86400):
        """PPT 상태 저장 (TTL 24시간)"""
        self.redis.setex(
            f"ppt:{ppt_id}",
            ttl,
            json.dumps(data)
        )
    
    async def get_ppt_status(self, ppt_id: str) -> Optional[dict]:
        """PPT 상태 조회"""
        data = self.redis.get(f"ppt:{ppt_id}")
        return json.loads(data) if data else None

    async def update_ppt_status(self, ppt_id: str, updates: dict, default_ttl: int = 86400):
        """Merge and update PPT status JSON in Redis.

        - Reads current JSON if present and merges with updates
        - Ensures updated_at is set
        - Preserves remaining TTL if available, else uses default_ttl
        """
        key = f"ppt:{ppt_id}"
        try:
            current = self.redis.get(key)
            obj = json.loads(current) if current else {}
        except Exception:
            obj = {}

        obj.update(updates or {})

        # Ensure updated_at present
        from datetime import datetime
        obj.setdefault("updated_at", datetime.utcnow().isoformat())
        
        # 진행 상태 로그 추가
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Updating PPT status for {ppt_id}: stage={updates.get('current_stage')}, progress={updates.get('progress')}%")

        # Preserve TTL where possible
        try:
            ttl = self.redis.ttl(key)
            if not isinstance(ttl, int) or ttl <= 0:
                ttl = default_ttl
        except Exception:
            ttl = default_ttl

        self.redis.setex(key, ttl, json.dumps(obj))
