"""
Redis 캐시 클라이언트
비동기 Redis 연결 및 캐싱 유틸리티
"""

import json
import hashlib
from typing import Any, Optional, Union
import redis.asyncio as redis
from app.core.config import settings
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis 캐시 관리자"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.is_connected = False
    
    async def connect(self):
        """Redis 연결 설정"""
        try:
            # redis.asyncio.from_url returns client synchronously
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                max_connections=20
            )
            # 연결 테스트
            await self.redis_client.ping()
            self.is_connected = True
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.is_connected = False
    
    async def disconnect(self):
        """Redis 연결 종료"""
        if self.redis_client:
            await self.redis_client.close()
            self.is_connected = False
            logger.info("Redis connection closed")
    
    def _generate_key(self, prefix: str, data: Any) -> str:
        """
        캐시 키 생성
        
        Args:
            prefix: 키 프리픽스
            data: 키 생성에 사용할 데이터
        
        Returns:
            str: 생성된 캐시 키
        """
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        
        hash_obj = hashlib.md5(data_str.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"
    
    async def get(self, key: str) -> Optional[Any]:
        """
        캐시에서 값 조회
        
        Args:
            key: 캐시 키
        
        Returns:
            캐시된 값 또는 None
        """
        if not self.is_connected:
            return None
        
        try:
            value = await self.redis_client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[Union[int, timedelta]] = None
    ) -> bool:
        """
        캐시에 값 저장
        
        Args:
            key: 캐시 키
            value: 저장할 값
            ttl: TTL (초 단위 또는 timedelta)
        
        Returns:
            bool: 저장 성공 여부
        """
        if not self.is_connected:
            return False
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            if ttl is None:
                ttl = 3600  # 기본 1시간
            elif isinstance(ttl, timedelta):
                ttl = int(ttl.total_seconds())
            
            await self.redis_client.setex(key, ttl, value)
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        캐시에서 키 삭제
        
        Args:
            key: 삭제할 키
        
        Returns:
            bool: 삭제 성공 여부
        """
        if not self.is_connected:
            return False
        
        try:
            result = await self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """
        키 존재 여부 확인
        
        Args:
            key: 확인할 키
        
        Returns:
            bool: 키 존재 여부
        """
        if not self.is_connected:
            return False
        
        try:
            return await self.redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False
    
    async def expire(self, key: str, ttl: Union[int, timedelta]) -> bool:
        """
        키의 TTL 설정
        
        Args:
            key: 대상 키
            ttl: TTL (초 단위 또는 timedelta)
        
        Returns:
            bool: 설정 성공 여부
        """
        if not self.is_connected:
            return False
        
        try:
            if isinstance(ttl, timedelta):
                ttl = int(ttl.total_seconds())
            
            return await self.redis_client.expire(key, ttl)
        except Exception as e:
            logger.error(f"Redis expire error: {e}")
            return False
    
    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """
        카운터 증가
        
        Args:
            key: 카운터 키
            amount: 증가량
        
        Returns:
            증가된 값 또는 None
        """
        if not self.is_connected:
            return None
        
        try:
            return await self.redis_client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Redis increment error: {e}")
            return None
    
    async def get_ttl(self, key: str) -> Optional[int]:
        """
        키의 남은 TTL 조회
        
        Args:
            key: 조회할 키
        
        Returns:
            남은 TTL (초) 또는 None
        """
        if not self.is_connected:
            return None
        
        try:
            ttl = await self.redis_client.ttl(key)
            return ttl if ttl >= 0 else None
        except Exception as e:
            logger.error(f"Redis TTL error: {e}")
            return None
    
    async def cache_llm_response(
        self,
        prompt: str,
        response: str,
        model: str = "gpt-4",
        ttl: int = 3600
    ) -> bool:
        """
        LLM 응답 캐싱
        
        Args:
            prompt: 프롬프트
            response: 응답
            model: 모델명
            ttl: TTL (초)
        
        Returns:
            bool: 캐싱 성공 여부
        """
        key = self._generate_key(f"llm:{model}", prompt)
        return await self.set(key, response, ttl)
    
    async def get_llm_response(self, prompt: str, model: str = "gpt-4") -> Optional[str]:
        """
        캐싱된 LLM 응답 조회
        
        Args:
            prompt: 프롬프트
            model: 모델명
        
        Returns:
            캐싱된 응답 또는 None
        """
        key = self._generate_key(f"llm:{model}", prompt)
        return await self.get(key)
    
    async def ping(self) -> bool:
        """
        Redis 연결 테스트
        
        Returns:
            bool: 연결 성공 여부
        """
        if not self.redis_client:
            return False
        
        try:
            await self.redis_client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            return False

# 싱글톤 인스턴스
redis_cache = RedisCache()

async def get_redis() -> RedisCache:
    """
    Redis 캐시 의존성 주입용
    
    Returns:
        RedisCache: Redis 캐시 인스턴스
    """
    if not redis_cache.is_connected:
        await redis_cache.connect()
    return redis_cache
