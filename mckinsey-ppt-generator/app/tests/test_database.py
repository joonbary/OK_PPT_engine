"""
데이터베이스 연결 테스트
PostgreSQL과 Redis 연결 확인
"""

import pytest
import asyncio
from app.db.session import get_db, test_connection, init_db
from app.db.redis_client import get_redis
from app.db.models import PPTGenerationJob, JobStatus
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

@pytest.mark.asyncio
async def test_database_connection():
    """PostgreSQL 연결 테스트"""
    
    # 연결 테스트
    is_connected = await test_connection()
    assert is_connected, "데이터베이스 연결 실패"
    
    # 세션 테스트
    async for db in get_db():
        assert db is not None
        assert isinstance(db, AsyncSession)
        
        # 간단한 쿼리 테스트
        result = await db.execute("SELECT 1")
        assert result.scalar() == 1
        break

@pytest.mark.asyncio
async def test_redis_connection():
    """Redis 연결 테스트"""
    
    redis = await get_redis()
    assert redis is not None
    
    # Ping 테스트
    is_connected = await redis.ping()
    assert is_connected, "Redis 연결 실패"
    
    # 기본 작업 테스트
    test_key = "test:key"
    test_value = "test_value"
    
    # Set
    success = await redis.set(test_key, test_value)
    assert success
    
    # Get
    retrieved = await redis.get(test_key)
    assert retrieved == test_value
    
    # Exists
    exists = await redis.exists(test_key)
    assert exists
    
    # Delete
    deleted = await redis.delete(test_key)
    assert deleted

@pytest.mark.asyncio
async def test_database_models():
    """데이터베이스 모델 테스트"""
    
    # 데이터베이스 초기화
    await init_db()
    
    async for db in get_db():
        # PPT 생성 작업 생성
        job = PPTGenerationJob(
            id=uuid.uuid4(),
            status=JobStatus.PENDING,
            input_document="테스트 문서 내용",
            num_slides=10,
            target_audience="executive",
            presentation_purpose="analysis"
        )
        
        db.add(job)
        await db.commit()
        
        # 조회
        result = await db.get(PPTGenerationJob, job.id)
        assert result is not None
        assert result.status == JobStatus.PENDING
        assert result.input_document == "테스트 문서 내용"
        
        # 업데이트
        result.status = JobStatus.IN_PROGRESS
        await db.commit()
        
        # 재조회
        updated = await db.get(PPTGenerationJob, job.id)
        assert updated.status == JobStatus.IN_PROGRESS
        
        # 삭제
        await db.delete(updated)
        await db.commit()
        
        # 삭제 확인
        deleted = await db.get(PPTGenerationJob, job.id)
        assert deleted is None
        break

@pytest.mark.asyncio
async def test_redis_caching():
    """Redis 캐싱 테스트"""
    
    redis = await get_redis()
    
    # LLM 응답 캐싱 테스트
    prompt = "테스트 프롬프트"
    response = "테스트 응답"
    model = "gpt-4"
    
    # 캐싱
    cached = await redis.cache_llm_response(prompt, response, model)
    assert cached
    
    # 조회
    retrieved = await redis.get_llm_response(prompt, model)
    assert retrieved == response
    
    # TTL 확인
    key = redis._generate_key(f"llm:{model}", prompt)
    ttl = await redis.get_ttl(key)
    assert ttl is not None
    assert ttl > 0
    
    # 카운터 테스트
    counter_key = "test:counter"
    count = await redis.increment(counter_key)
    assert count == 1
    
    count = await redis.increment(counter_key, 5)
    assert count == 6
    
    # 정리
    await redis.delete(counter_key)

if __name__ == "__main__":
    # 동기적으로 테스트 실행
    async def run_tests():
        print("데이터베이스 연결 테스트 시작...")
        
        try:
            await test_database_connection()
            print("✅ PostgreSQL 연결 테스트 통과")
        except Exception as e:
            print(f"❌ PostgreSQL 연결 테스트 실패: {e}")
        
        try:
            await test_redis_connection()
            print("✅ Redis 연결 테스트 통과")
        except Exception as e:
            print(f"❌ Redis 연결 테스트 실패: {e}")
        
        try:
            await test_database_models()
            print("✅ 데이터베이스 모델 테스트 통과")
        except Exception as e:
            print(f"❌ 데이터베이스 모델 테스트 실패: {e}")
        
        try:
            await test_redis_caching()
            print("✅ Redis 캐싱 테스트 통과")
        except Exception as e:
            print(f"❌ Redis 캐싱 테스트 실패: {e}")
        
        print("\n모든 테스트 완료!")
    
    asyncio.run(run_tests())