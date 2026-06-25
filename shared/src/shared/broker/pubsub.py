"""
Redis Pub/Sub — обёртка для публикации и подписки на каналы.

Publish:
    await pubsub_publish("tasks:123", {"status": "completed", "progress": 100})

Subscribe (async generator):
    async for message in pubsub_subscribe("tasks:123"):
        print(message)  # dict
"""

import asyncio
import json
from collections.abc import AsyncGenerator

import redis.asyncio as redis


async def pubsub_publish(channel: str, data: dict, redis_client: redis.Redis) -> int:
    """Публикует JSON-сообщение в канал. Возвращает кол-во подписчиков, получивших сообщение."""
    return await redis_client.publish(channel, json.dumps(data))


async def pubsub_subscribe(
    channel: str,
    redis_client: redis.Redis,
    *,
    poll_interval: float = 0.1,
) -> AsyncGenerator[dict, None]:
    """Подписывается на канал и yield'ит десериализованные сообщения.

    Корректно отписывается при выходе из генератора (break / исключение).
    """
    ps = redis_client.pubsub()
    await ps.subscribe(channel)

    try:
        while True:
            msg = await ps.get_message(ignore_subscribe_messages=True, timeout=poll_interval)
            if msg is not None and msg["type"] == "message":
                yield json.loads(msg["data"])
            else:
                await asyncio.sleep(poll_interval)
    finally:
        await ps.unsubscribe(channel)
        await ps.aclose()
