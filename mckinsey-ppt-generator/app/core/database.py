from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import Generator, Optional
import asyncpg
from asyncpg.pool import Pool
import asyncio
from .config import settings

# SQLAlchemy setup
if settings.DATABASE_URL and settings.DATABASE_URL.startswith("postgresql"):
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://"
    )
elif settings.DATABASE_URL and settings.DATABASE_URL.startswith("sqlite"):
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create engine with SQLite compatibility
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},  # SQLite specific
        echo=True if settings.APP_ENV == "development" else False,
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=NullPool,
        echo=True if settings.APP_ENV == "development" else False,
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Async PostgreSQL connection pool
async_pool: Optional[Pool] = None

async def init_db_pool():
    """Initialize async database connection pool"""
    global async_pool
    # Only initialize pool for PostgreSQL
    if settings.DATABASE_URL and settings.DATABASE_URL.startswith("postgresql"):
        try:
            async_pool = await asyncpg.create_pool(
                settings.DATABASE_URL,
                min_size=10,
                max_size=20,
                max_queries=50000,
                max_inactive_connection_lifetime=300.0,
            )
            return async_pool
        except Exception as e:
            print(f"Failed to create async pool: {e}")
    return None

async def close_db_pool():
    """Close database connection pool"""
    global async_pool
    if async_pool:
        await async_pool.close()

# Dependency to get DB session
def get_db() -> Generator:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """Get async database connection"""
    global async_pool
    if not async_pool:
        await init_db_pool()
    
    async with async_pool.acquire() as connection:
        async with connection.transaction():
            yield connection