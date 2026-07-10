"""API dependencies."""

from fastapi import Request

from app.leaderboard.service import LeaderboardService


def get_leaderboard_service(request: Request) -> LeaderboardService:
    return request.app.state.leaderboard_service
