"""API dependencies."""

from fastapi import Request

from app.leaderboard.manager import ConnectionManager
from app.leaderboard.service import LeaderboardService


def get_leaderboard_service(request: Request) -> LeaderboardService:
    return request.app.state.leaderboard_service


def get_connection_manager(request: Request) -> ConnectionManager:
    return request.app.state.connection_manager
