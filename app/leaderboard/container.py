"""Leaderboard composition helpers."""

from redis.asyncio import Redis
from app.core.config import Settings
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.leaderboard.repository import PostgresLeaderboardRepository
from app.leaderboard.service import LeaderboardService


def build_leaderboard_service(
    settings: Settings,
    redis_client: Redis,
    session_factory: async_sessionmaker[AsyncSession],
) -> LeaderboardService:
    repository = PostgresLeaderboardRepository(
        session_factory=session_factory,
        leaderboard_size=settings.leaderboard_size,
    )
    return LeaderboardService(
        repository=repository,
        redis_client=redis_client,
        settings=settings,
    )
