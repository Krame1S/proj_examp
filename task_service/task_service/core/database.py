import asyncpg
import redis.asyncio as redis

from task_service.core.config import settings

_pool: asyncpg.Pool | None = None
_redis: redis.Redis | None = None


async def get_db_pool() -> asyncpg.Pool:
    global _pool  # noqa: PLW0603
    if _pool is None:
        _pool = await asyncpg.create_pool(
            dsn=settings.DATABASE_URL,
            min_size=settings.DB_MIN_POOL_SIZE,
            max_size=settings.DB_MAX_POOL_SIZE,
            server_settings={"search_path": settings.DB_SCHEMA},
        )
    return _pool


async def close_db_pool() -> None:
    global _pool  # noqa: PLW0603
    if _pool is not None:
        await _pool.close()
        _pool = None


def get_redis_client() -> redis.Redis:
    global _redis  # noqa: PLW0603
    if _redis is None:
        _redis = redis.from_url(settings.REDIS_URL)
    return _redis


async def close_redis_client() -> None:
    global _redis  # noqa: PLW0603
    if _redis is not None:
        await _redis.aclose()
        _redis = None
