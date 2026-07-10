"""SQLAlchemy models for leaderboard storage."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LeaderboardPlayer(Base):
    __tablename__ = "leaderboard_players"

    player_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    player_name: Mapped[str] = mapped_column(String(64), nullable=False)
    score: Mapped[int] = mapped_column(nullable=False, default=0)
