"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.database import Base, create_engine, create_session_factory
from app.core.logging import configure_logging
from app.core.redis import create_redis_client
from app.leaderboard.container import build_leaderboard_service
from app.leaderboard.manager import ConnectionManager
from app.leaderboard import models as leaderboard_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = create_engine(settings)
    session_factory = create_session_factory(engine)
    redis_client = create_redis_client(settings)
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
    app.state.redis = redis_client
    app.state.connection_manager = ConnectionManager()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    app.state.leaderboard_service = build_leaderboard_service(settings, session_factory)
    try:
        yield
    finally:
        await redis_client.aclose()
        await engine.dispose()


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
