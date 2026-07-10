"""Shared application settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Real-Time Leaderboard API"
    app_version: str = "0.1.0"
    redis_url: str = "redis://localhost:6379/0"
    redis_leaderboard_channel: str = "leaderboard:updates"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/realtime_leaderboard"
    leaderboard_size: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LEADERBOARD_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
