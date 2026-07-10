from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.router import api_router
from app.leaderboard.schemas import (
    LeaderboardEntry,
    LeaderboardResponse,
    PlayerRankResponse,
    ScoreSubmissionResponse,
    utcnow,
)


class StubLeaderboardService:
    async def get_leaderboard(self) -> LeaderboardResponse:
        return LeaderboardResponse(
            entries=[
                LeaderboardEntry(
                    player_id="player-1",
                    player_name="Alice",
                    score=120,
                    rank=1,
                )
            ],
            updated_at=utcnow(),
        )

    async def get_player_rank(self, player_id: str) -> PlayerRankResponse | None:
        if player_id != "player-1":
            return None
        return PlayerRankResponse(
            player=LeaderboardEntry(
                player_id="player-1",
                player_name="Alice",
                score=120,
                rank=1,
            ),
            updated_at=utcnow(),
        )

    async def submit_score(self, payload) -> ScoreSubmissionResponse:
        return ScoreSubmissionResponse(
            player=LeaderboardEntry(
                player_id=payload.player_id,
                player_name=payload.player_name,
                score=payload.score_delta,
                rank=1,
            ),
            submitted_at=utcnow(),
        )


def build_test_client() -> TestClient:
    app = FastAPI()
    app.include_router(api_router)
    app.state.leaderboard_service = StubLeaderboardService()
    return TestClient(app)


def test_healthcheck() -> None:
    client = build_test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_leaderboard() -> None:
    client = build_test_client()
    response = client.get("/api/v1/leaderboard")

    assert response.status_code == 200
    payload = response.json()
    assert payload["entries"][0]["player_id"] == "player-1"
    assert payload["entries"][0]["rank"] == 1


def test_get_missing_player_rank() -> None:
    client = build_test_client()
    response = client.get("/api/v1/leaderboard/missing-player")

    assert response.status_code == 404
    assert response.json()["detail"] == "Player 'missing-player' was not found."


def test_submit_score() -> None:
    client = build_test_client()
    response = client.post(
        "/api/v1/leaderboard/scores",
        json={
            "player_id": "player-2",
            "player_name": "Bob",
            "score_delta": 55,
        },
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["player"]["player_id"] == "player-2"
    assert payload["player"]["score"] == 55
