"""Leaderboard repository abstractions and PostgreSQL implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy import Select, desc, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.leaderboard.models import LeaderboardPlayer
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


class PostgresLeaderboardRepository(LeaderboardRepository):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        leaderboard_size: int = 10,
    ) -> None:
        self._session_factory = session_factory
        self._leaderboard_size = leaderboard_size

    async def get_entries(self) -> list[LeaderboardEntry]:
        async with self._session_factory() as session:
            players = await self._fetch_ranked_players(session)
            return [
                self._to_entry(player=player, rank=index)
                for index, player in enumerate(players[: self._leaderboard_size], start=1)
            ]

    async def get_player(self, player_id: str) -> LeaderboardEntry | None:
        async with self._session_factory() as session:
            players = await self._fetch_ranked_players(session)
            for index, player in enumerate(players, start=1):
                if player.player_id == player_id:
                    return self._to_entry(player=player, rank=index)
        return None

    async def submit_score(
        self,
        player_id: str,
        player_name: str,
        score_delta: int,
    ) -> LeaderboardEntry:
        async with self._session_factory() as session:
            player = await session.get(LeaderboardPlayer, player_id)
            if player is None:
                player = LeaderboardPlayer(
                    player_id=player_id,
                    player_name=player_name,
                    score=score_delta,
                )
                session.add(player)
            else:
                player.player_name = player_name
                player.score += score_delta

            await session.commit()

            players = await self._fetch_ranked_players(session)
            for index, ranked_player in enumerate(players, start=1):
                if ranked_player.player_id == player_id:
                    return self._to_entry(player=ranked_player, rank=index)

        raise RuntimeError("Submitted player was not found after commit.")

    async def _fetch_ranked_players(
        self,
        session: AsyncSession,
    ) -> list[LeaderboardPlayer]:
        statement: Select[tuple[LeaderboardPlayer]] = (
            select(LeaderboardPlayer)
            .order_by(
                desc(LeaderboardPlayer.score),
                LeaderboardPlayer.player_name,
                LeaderboardPlayer.player_id,
            )
        )
        result = await session.execute(statement)
        return list(result.scalars().all())

    @staticmethod
    def _to_entry(player: LeaderboardPlayer, rank: int) -> LeaderboardEntry:
        return LeaderboardEntry(
            player_id=player.player_id,
            player_name=player.player_name,
            score=player.score,
            rank=rank,
        )
