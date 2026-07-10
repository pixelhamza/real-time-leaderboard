"""Top-level API router."""

from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.leaderboard import router as leaderboard_router
from app.api.routes.websocket import router as websocket_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(leaderboard_router, prefix="/api/v1")
api_router.include_router(websocket_router)
