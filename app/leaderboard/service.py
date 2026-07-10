"""Leaderboard service layer."""

from dataclasses import dataclass

from redis.asyncio import Redis

from app.core.config import Settings
from app.leaderboard.events import publish_leaderboard_update
from app.leaderboard.repository import LeaderboardRepository
from app.leaderboard.schemas import (
    LeaderboardResponse,
    PlayerRankResponse,
    ScoreSubmission,
    ScoreSubmissionResponse,
    utcnow,
)


@dataclass(slots=True)
class LeaderboardService:
    repository: LeaderboardRepository
    redis_client: Redis
    settings: Settings

    async def get_leaderboard(self) -> LeaderboardResponse:
        entries = await self.repository.get_entries()
        return LeaderboardResponse(entries=entries, updated_at=utcnow())

    async def get_player_rank(self, player_id: str) -> PlayerRankResponse | None:
        player = await self.repository.get_player(player_id)
        if player is None:
            return None
        return PlayerRankResponse(player=player, updated_at=utcnow())

    async def submit_score(self, payload: ScoreSubmission) -> ScoreSubmissionResponse:
        player = await self.repository.submit_score(
            player_id=payload.player_id,
            player_name=payload.player_name,
            score_delta=payload.score_delta,
        )
        leaderboard = await self.get_leaderboard()
        await publish_leaderboard_update(
            self.redis_client,
            self.settings.redis_leaderboard_channel,
            leaderboard.model_dump(mode="json"),
        )
        return ScoreSubmissionResponse(player=player, submitted_at=utcnow())
