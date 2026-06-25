import json
from typing import Annotated

import redis.asyncio as redis
from fastapi import APIRouter, Depends, Request
from shared.broker.pubsub import pubsub_subscribe
from sse_starlette.sse import EventSourceResponse

from gateway.api.deps import get_current_user_id, get_redis

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stream")
async def dashboard_stream(
    request: Request,
    user_id: Annotated[int, Depends(get_current_user_id)],
    redis_client: Annotated[redis.Redis, Depends(get_redis)],  # noqa: B008
) -> EventSourceResponse:
    async def generator():
        async for data in pubsub_subscribe(f"dashboard:{user_id}", redis_client):
            if await request.is_disconnected():
                break
            yield {"data": json.dumps(data)}

    return EventSourceResponse(generator())
