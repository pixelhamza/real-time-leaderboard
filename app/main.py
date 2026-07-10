"""FastAPI application entrypoint."""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.database import Base, create_engine, create_session_factory
from app.core.logging import configure_logging
from app.core.redis import create_redis_client
from app.leaderboard.events import consume_leaderboard_updates
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
    app.state.leaderboard_service = build_leaderboard_service(
        settings,
        redis_client,
        session_factory,
    )
    listener_task = asyncio.create_task(
        consume_leaderboard_updates(
            redis_client,
            settings.redis_leaderboard_channel,
            app.state.connection_manager,
        )
    )
    app.state.redis_listener_task = listener_task
    try:
        yield
    finally:
        listener_task.cancel()
        await asyncio.gather(listener_task, return_exceptions=True)
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
