"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.redis import create_redis_client
from app.leaderboard.container import build_leaderboard_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    redis_client = create_redis_client(settings)
    app.state.redis = redis_client
    app.state.leaderboard_service = build_leaderboard_service(settings)
    try:
        yield
    finally:
        await redis_client.aclose()


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    app.include_router(api_router)
    return app


app = create_app()
