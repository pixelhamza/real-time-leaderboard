"""Leaderboard repository abstractions."""

from abc import ABC, abstractmethod

from app.leaderboard.schemas import LeaderboardEntry


class LeaderboardRepository(ABC):
    @abstractmethod
    async def get_entries(self) -> list[LeaderboardEntry]:
        raise NotImplementedError

    @abstractmethod
    async def get_player(self, player_id: str) -> LeaderboardEntry | None:
        raise NotImplementedError

    @abstractmethod
    async def submit_score(
        self,
        player_id: str,
        player_name: str,
        score_delta: int,
    ) -> LeaderboardEntry:
        raise NotImplementedError
