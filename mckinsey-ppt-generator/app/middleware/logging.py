from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import uuid
from app.core.logging import app_logger

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all API requests and responses"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Start time
        start_time = time.time()
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Log request
        app_logger.bind(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=0,
            process_time=0,
        ).info(f"Request started: {request.method} {request.url.path}")
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error
            process_time = int((time.time() - start_time) * 1000)
            app_logger.bind(
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=500,
                process_time=process_time,
            ).error(f"Request failed: {str(e)}")
            raise
        
        # Calculate process time
        process_time = int((time.time() - start_time) * 1000)
        
        # Add headers to response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log response
        app_logger.bind(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time=process_time,
        ).info(f"Request completed: {response.status_code}")
        
        return response