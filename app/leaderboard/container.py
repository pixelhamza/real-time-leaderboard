"""Leaderboard composition helpers."""

from app.core.config import Settings
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.leaderboard.repository import PostgresLeaderboardRepository
from app.leaderboard.service import LeaderboardService


def build_leaderboard_service(
    settings: Settings,
    session_factory: async_sessionmaker[AsyncSession],
) -> LeaderboardService:
    repository = PostgresLeaderboardRepository(
        session_factory=session_factory,
        leaderboard_size=settings.leaderboard_size,
    )
    return LeaderboardService(repository=repository)
