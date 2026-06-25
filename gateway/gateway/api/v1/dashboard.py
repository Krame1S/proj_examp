from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse
from gateway.api.deps import get_current_user_id, get_redis
from shared.broker.pubsub import pubsub_subscribe
import json

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])



@router.get("/stream")
async def dashboard_stream(
    request: Request,
    user_id: int = Depends(get_current_user_id),
    redis_client=Depends(get_redis),
):
    async def generator():
        async for data in pubsub_subscribe(f"dashboard:{user_id}", redis_client):
            if await request.is_disconnected():
                break
            yield {"data": json.dumps(data)}

    return EventSourceResponse(generator())