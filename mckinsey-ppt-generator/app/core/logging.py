from loguru import logger
import sys
import os
from pathlib import Path
from .config import settings

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Remove default handler
logger.remove()

# Console handler with color
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL,
)

# File handler for all logs
logger.add(
    log_dir / "app.log",
    rotation="00:00",  # Rotate at midnight
    retention="30 days",  # Keep logs for 30 days
    compression="zip",  # Compress rotated logs
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    enqueue=True,  # Thread-safe logging
)

# File handler for error logs only
logger.add(
    log_dir / "error.log",
    rotation="1 week",
    retention="3 months",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    enqueue=True,
    backtrace=True,  # Include stack trace
    diagnose=True,   # Include variable values
)

# File handler for API requests
logger.add(
    log_dir / "api.log",
    rotation="100 MB",  # Rotate when file size exceeds 100MB
    retention="1 week",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[request_id]} | {extra[method]} | {extra[path]} | {extra[status_code]} | {extra[process_time]}ms - {message}",
    level="INFO",
    filter=lambda record: "request_id" in record["extra"],  # Only log records with request_id
    enqueue=True,
)

# Development-specific logging
if settings.APP_ENV == "development":
    logger.add(
        log_dir / "debug.log",
        rotation="50 MB",
        retention="3 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        enqueue=True,
    )

def get_logger(name: str = None):
    """Get a logger instance with a specific name"""
    if name:
        return logger.bind(name=name)
    return logger

# Create logger instance for import
app_logger = get_logger("app")