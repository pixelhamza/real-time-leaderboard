"""Redis-backed leaderboard event publishing and subscription."""

from __future__ import annotations

import asyncio
import json
import logging

from redis.asyncio import Redis

from app.leaderboard.manager import ConnectionManager

logger = logging.getLogger(__name__)


async def publish_leaderboard_update(
    redis_client: Redis,
    channel: str,
    payload: dict,
) -> None:
    await redis_client.publish(channel, json.dumps(payload))


async def consume_leaderboard_updates(
    redis_client: Redis,
    channel: str,
    manager: ConnectionManager,
) -> None:
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)
    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            data = json.loads(message["data"])
            await manager.broadcast(data)
    except asyncio.CancelledError:
        raise
    except Exception:
        logger.exception("Leaderboard update consumer stopped unexpectedly.")
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.aclose()
