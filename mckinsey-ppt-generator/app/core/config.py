from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application Settings
    APP_NAME: str = "McKinsey PPT Generator"
    APP_ENV: str = "development"
    VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"

    # API 설정
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: Optional[str] = "postgresql://postgres:postgres@localhost:5432/ppt_db"
    
    # Redis
    REDIS_URL: Optional[str] = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # LLM API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    OUTPUT_DIR: str = "./output"
    MAX_FILE_SIZE_MB: int = 10
    PPT_STORAGE_PATH: str = "/tmp/ppt_files"

    # PPT Generation Settings
    DEFAULT_TEMPLATE: str = "McKinsey Professional"
    MAX_SLIDES_PER_PRESENTATION: int = 100
    ENABLE_AI_ENHANCEMENT: bool = True
    MAX_CONCURRENT_JOBS: int = 10
    PPT_GENERATION_TIMEOUT: int = 300  # 5분

    # Logging
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env

# Create settings instance
settings = Settings()
