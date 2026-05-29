import datetime as dt
import logging
import uuid

import jwt
import redis.asyncio as redis
from passlib.hash import argon2

from user_service.core.config import settings
from user_service.exceptions.auth import InvalidToken, TokenExpired

logger = logging.getLogger(__name__)

_private_key: str | None = None
_public_key: str | None = None


def load_keys() -> None:
    global _private_key, _public_key
    try:
        with open(settings.JWT_PRIVATE_KEY_PATH) as f:
            _private_key = f.read()
        with open(settings.JWT_PUBLIC_KEY_PATH) as f:
            _public_key = f.read()
    except Exception as e:
        raise RuntimeError("Failed to load JWT keys") from e


def hash_password(password: str) -> str:
    return argon2.using(
        memory_cost=131072,
        time_cost=3,
        parallelism=4,
        salt_len=64,
        digest_size=64,
    ).hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return argon2.verify(password, hashed)


def create_access_token(user_id: int) -> str:
    if _private_key is None:
        raise RuntimeError("JWT private key not loaded")
    now = dt.datetime.now(dt.UTC)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + dt.timedelta(seconds=settings.ACCESS_TOKEN_LIFETIME),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, _private_key, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    if _private_key is None:
        raise RuntimeError("JWT private key not loaded")
    now = dt.datetime.now(dt.UTC)
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": now,
        "exp": now + dt.timedelta(seconds=settings.REFRESH_TOKEN_LIFETIME),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, _private_key, algorithm=settings.JWT_ALGORITHM)


async def decode_refresh_token(token: str, redis_client: redis.Redis) -> int:
    if _public_key is None:
        raise RuntimeError("JWT public key not loaded")
    try:
        payload = jwt.decode(token, _public_key, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as e:
        raise TokenExpired() from e
    except jwt.InvalidTokenError as e:
        raise InvalidToken() from e

    if payload.get("type") != "refresh":
        raise InvalidToken()

    user_id = int(payload["sub"])
    jti = payload["jti"]
    key = f"user:{user_id}:refresh:{jti}"
    exists = await redis_client.delete(key)
    if not exists:
        raise InvalidToken()

    return user_id


async def store_refresh_token(user_id: int, token: str, redis_client: redis.Redis) -> None:
    if _public_key is None:
        raise RuntimeError("JWT public key not loaded")
    payload = jwt.decode(token, _public_key, algorithms=[settings.JWT_ALGORITHM])
    jti = payload["jti"]
    key = f"user:{user_id}:refresh:{jti}"
    await redis_client.setex(key, settings.REFRESH_TOKEN_LIFETIME, "1")