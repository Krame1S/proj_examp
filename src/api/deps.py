"""Centralized dependency injection — the architectural core of the template."""

from collections.abc import AsyncGenerator
from typing import Annotated

import asyncpg
import redis.asyncio as redis
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.security import decode_access_token
from src.db.pool import get_db_pool
from src.repository.user import UserRepository
from src.repository.task import TaskRepository
from src.service.auth import AuthService
from src.service.user import UserService
from src.service.task import TaskService
from asyncpg.pool import PoolConnectionProxy
from src.repository.category import CategoryRepository
from src.service.category import CategoryService

security_scheme = HTTPBearer()

# ── Infrastructure dependencies ──────────────────────────

redis_client: redis.Redis | None = None


async def get_db() -> AsyncGenerator[PoolConnectionProxy, None]:
    db_pool = get_db_pool()
    if db_pool is None:
        raise RuntimeError("Database pool not initialized")
    async with db_pool.acquire() as conn:
        yield conn


def get_redis() -> redis.Redis | None:
    return redis_client


# ── Auth dependency ──────────────────────────────────────


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
) -> int:
    return decode_access_token(credentials.credentials)


# ── Repository dependencies ──────────────────────────────


async def get_user_repository(
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> UserRepository:
    return UserRepository(conn)

async def get_task_repository(
    conn: Annotated[asyncpg.Connection, Depends(get_db)]
) -> TaskRepository:
    return TaskRepository(conn)

async def get_category_repository(
    conn: Annotated[asyncpg.Connection, Depends(get_db)]
) -> CategoryRepository:
    return CategoryRepository(conn)


# ── Service dependencies ─────────────────────────────────


async def get_auth_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    redis_conn: Annotated[redis.Redis, Depends(get_redis)],
) -> AuthService:
    return AuthService(repo, redis_conn)


async def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repo)

async def get_task_service(
    repo: Annotated[TaskRepository, Depends(get_task_repository)]
) -> TaskService:
    return TaskService(repo)

async def get_category_service(
    repo: Annotated[CategoryRepository, Depends(get_category_repository)]
) -> CategoryService:
    return CategoryService(repo)