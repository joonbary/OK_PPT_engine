"""
데이터베이스 세션 관리
PostgreSQL 비동기 연결 및 세션 팩토리
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# 데이터베이스 연결 URL을 비동기 드라이버에 맞게 변환
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL:
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("sqlite"):
        DATABASE_URL = DATABASE_URL.replace("sqlite", "sqlite+aiosqlite", 1)

# 비동기 엔진 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.APP_ENV == "development",  # 개발 환경에서만 SQL 출력
    future=True,
    pool_pre_ping=True,  # 연결 검증
)

# 비동기 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base 클래스 (모델 정의용)
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    데이터베이스 세션 의존성 주입용
    
    Yields:
        AsyncSession: 비동기 데이터베이스 세션
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """
    데이터베이스 초기화
    테이블 생성 및 초기 데이터 설정
    """
    try:
        async with engine.begin() as conn:
            # 테이블 생성
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

async def close_db():
    """
    데이터베이스 연결 종료
    """
    await engine.dispose()
    logger.info("Database connection closed")

# 연결 테스트 함수
async def test_connection():
    """
    데이터베이스 연결 테스트
    
    Returns:
        bool: 연결 성공 여부
    """
    try:
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            return result.scalar() == 1
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False