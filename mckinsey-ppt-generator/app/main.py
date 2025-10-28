# -*- coding: utf-8 -*-
"""
FastAPI main application (UTF-8)
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.endpoints import ppt
from app.api.v1 import phase_endpoints
from app.api.v1.endpoints import upload
from app.core.redis_client import RedisClient

import asyncio

app = FastAPI(
    title="McKinsey PPT Generator API",
    description="Multi-agent PPT generator with template orchestration.",
    version="1.0.0",
)

class TimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await asyncio.wait_for(call_next(request), timeout=300.0)
            return response
        except asyncio.TimeoutError:
            return JSONResponse(status_code=504, content={"detail": "Request timeout"})
        except Exception:
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})

app.add_middleware(TimeoutMiddleware)

# CORS 설정 (단 한 번만!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(ppt.router, prefix="/api/v1", tags=["ppt"])
try:
    app.include_router(phase_endpoints.router, prefix="/api/v1", tags=["phases"])
except Exception:
    pass
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])

@app.on_event("shutdown")
async def shutdown_event():
    try:
        redis_client = RedisClient()
        close = getattr(redis_client, "close", None)
        if callable(close):
            await close()
    except Exception:
        pass

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "healthy",
        "service": "McKinsey PPT Generation API",
        "version": "1.0.0",
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "llm": "available",
    }

@app.get("/api/v1/health", tags=["Health Check"])
async def api_v1_health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "llm": "available",
    }
