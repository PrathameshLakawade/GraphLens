"""Top-level API router."""

from fastapi import APIRouter

from server.app.api.routes.health import router as health_router
from server.app.api.routes.query import router as query_router
from server.app.api.routes.transcripts import router as transcripts_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(query_router, tags=["query"])
api_router.include_router(transcripts_router, tags=["transcripts"])
