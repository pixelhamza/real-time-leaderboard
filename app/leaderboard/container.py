"""Leaderboard composition helpers."""

from app.core.config import Settings
from app.leaderboard.repository import InMemoryLeaderboardRepository
from app.leaderboard.service import LeaderboardService


def build_leaderboard_service(settings: Settings) -> LeaderboardService:
    repository = InMemoryLeaderboardRepository(
        leaderboard_size=settings.leaderboard_size,
    )
    return LeaderboardService(repository=repository)
