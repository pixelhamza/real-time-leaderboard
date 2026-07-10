# Real-Time Leaderboard API

FastAPI backend for a real-time leaderboard with PostgreSQL persistence and Redis-backed live updates.

## Stack

- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy async
- WebSocket leaderboard feed

## Structure

```text
app/
  api/
    routes/
  core/
  leaderboard/
tests/
```

## Local Setup

1. Create a virtual environment.
2. Install dependencies with `pip install -e ".[dev]"`.
3. Create a `.env` file from `.env.example`.
4. Start PostgreSQL.
5. Start Redis.
6. Run `uvicorn app.main:app --reload`.

## Environment

```env
LEADERBOARD_APP_NAME=Real-Time Leaderboard API
LEADERBOARD_REDIS_URL=redis://localhost:6379/0
LEADERBOARD_REDIS_LEADERBOARD_CHANNEL=leaderboard:updates
LEADERBOARD_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/realtime_leaderboard
LEADERBOARD_LEADERBOARD_SIZE=10
```

## API

- `GET /health`
- `GET /api/v1/leaderboard`
- `GET /api/v1/leaderboard/{player_id}`
- `POST /api/v1/leaderboard/scores`
- `WS /ws/leaderboard`

## Notes

- Tables are created automatically on startup.
- Alembic is intentionally not included.
- WebSocket clients receive an initial snapshot and live updates after score submissions.
