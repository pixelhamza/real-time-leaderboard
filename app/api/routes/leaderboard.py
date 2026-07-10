"""Leaderboard REST routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_leaderboard_service
from app.leaderboard.schemas import (
    LeaderboardResponse,
    PlayerRankResponse,
    ScoreSubmission,
    ScoreSubmissionResponse,
)
from app.leaderboard.service import LeaderboardService

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=LeaderboardResponse)
async def get_leaderboard(
    service: LeaderboardService = Depends(get_leaderboard_service),
) -> LeaderboardResponse:
    return await service.get_leaderboard()


@router.get("/{player_id}", response_model=PlayerRankResponse)
async def get_player_rank(
    player_id: str,
    service: LeaderboardService = Depends(get_leaderboard_service),
) -> PlayerRankResponse:
    player = await service.get_player_rank(player_id)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player '{player_id}' was not found.",
        )
    return player


@router.post(
    "/scores",
    response_model=ScoreSubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def submit_score(
    payload: ScoreSubmission,
    service: LeaderboardService = Depends(get_leaderboard_service),
) -> ScoreSubmissionResponse:
    return await service.submit_score(payload)
