"""Leaderboard domain schemas."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class ScoreSubmission(BaseModel):
    player_id: str = Field(min_length=1, max_length=64)
    player_name: str = Field(min_length=1, max_length=64)
    score_delta: int = Field(gt=0, le=1_000_000)

    @field_validator("player_id", "player_name")
    @classmethod
    def strip_value(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("value must not be blank")
        return stripped


class LeaderboardEntry(BaseModel):
    player_id: str
    player_name: str
    score: int = Field(ge=0)
    rank: int = Field(ge=1)


class LeaderboardResponse(BaseModel):
    entries: list[LeaderboardEntry]
    updated_at: datetime


class PlayerRankResponse(BaseModel):
    player: LeaderboardEntry
    updated_at: datetime


class ScoreSubmissionResponse(BaseModel):
    accepted: bool = True
    player: LeaderboardEntry
    submitted_at: datetime


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
