"""Leaderboard repository abstractions and in-memory implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from asyncio import Lock
from collections.abc import Iterable

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


class InMemoryLeaderboardRepository(LeaderboardRepository):
    def __init__(self, leaderboard_size: int = 10) -> None:
        self._leaderboard_size = leaderboard_size
        self._players: dict[str, LeaderboardEntry] = {}
        self._lock = Lock()

    async def get_entries(self) -> list[LeaderboardEntry]:
        async with self._lock:
            return list(self._sorted_entries())[: self._leaderboard_size]

    async def get_player(self, player_id: str) -> LeaderboardEntry | None:
        async with self._lock:
            return self._players.get(player_id)

    async def submit_score(
        self,
        player_id: str,
        player_name: str,
        score_delta: int,
    ) -> LeaderboardEntry:
        async with self._lock:
            current = self._players.get(player_id)
            score = score_delta if current is None else current.score + score_delta
            self._players[player_id] = LeaderboardEntry(
                player_id=player_id,
                player_name=player_name,
                score=score,
                rank=1,
            )
            self._refresh_ranks()
            return self._players[player_id]

    def _refresh_ranks(self) -> None:
        for index, entry in enumerate(self._sorted_entries(), start=1):
            self._players[entry.player_id] = entry.model_copy(update={"rank": index})

    def _sorted_entries(self) -> Iterable[LeaderboardEntry]:
        return sorted(
            self._players.values(),
            key=lambda entry: (-entry.score, entry.player_name.lower(), entry.player_id),
        )
