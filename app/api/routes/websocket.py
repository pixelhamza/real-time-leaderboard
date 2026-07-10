"""Leaderboard WebSocket routes."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.leaderboard.manager import ConnectionManager
from app.leaderboard.service import LeaderboardService

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/leaderboard")
async def leaderboard_feed(websocket: WebSocket) -> None:
    manager: ConnectionManager = websocket.app.state.connection_manager
    service: LeaderboardService = websocket.app.state.leaderboard_service

    await manager.connect(websocket)
    try:
        snapshot = await service.get_leaderboard()
        await manager.send_json(
            websocket,
            snapshot.model_dump(mode="json"),
        )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
