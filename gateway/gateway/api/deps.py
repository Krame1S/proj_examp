from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from gateway.core.config import settings
from gateway.core.security import decode_access_token

security_scheme = HTTPBearer()


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
) -> int:
    return decode_access_token(credentials.credentials)


def get_redis() -> redis.Redis:
    return redis.from_url(settings.REDIS_URL)
