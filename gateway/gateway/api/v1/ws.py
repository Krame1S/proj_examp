import asyncio
import json
import logging
from contextlib import suppress

import redis.asyncio as redis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from shared.broker.queues import ConsumerQueue

from gateway.broker.rpc_publisher import rpc_publisher
from gateway.core.config import settings
from gateway.core.security import decode_access_token

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ws"])

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

MAX_CONTENT_LENGTH = 4000


class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, set[WebSocket]] = {}
        self.queues: dict[WebSocket, asyncio.Queue[dict]] = {}

    def join(self, room_id: str, ws: WebSocket):
        self.rooms.setdefault(room_id, set()).add(ws)
        self.queues[ws] = asyncio.Queue(maxsize=50)

    def leave(self, room_id: str, ws: WebSocket):
        self.rooms.get(room_id, set()).discard(ws)
        self.queues.pop(ws, None)
        if not self.rooms.get(room_id):
            self.rooms.pop(room_id, None)

    async def send_local(self, ws: WebSocket, msg: dict):
        queue = self.queues.get(ws)
        if not queue:
            return
        try:
            queue.put_nowait(msg)
        except asyncio.QueueFull:
            await ws.close(code=1011)

    async def broadcast_local(self, room_id: str, msg: dict):
        for ws in list(self.rooms.get(room_id, set())):
            await self.send_local(ws, msg)

    async def sender(self, ws: WebSocket):
        queue = self.queues[ws]
        while True:
            msg = await queue.get()
            await ws.send_json(msg)


manager = ConnectionManager()


async def publish_room(room_id: str, msg: dict):
    await redis_client.publish(f"room:{room_id}", json.dumps(msg))


async def redis_listener():
    pubsub = redis_client.pubsub()
    await pubsub.psubscribe("room:*")
    async for event in pubsub.listen():
        if event["type"] != "pmessage":
            continue
        room_id = event["channel"].split(":", 1)[1]
        msg = json.loads(event["data"])
        await manager.broadcast_local(room_id, msg)


async def rpc_call(queue: ConsumerQueue, payload: dict) -> dict:
    """Call chat_service over RPC and return the decoded JSON body."""
    raw = await rpc_publisher.call(
        message=json.dumps(payload),
        request_queue_name=queue.value,
    )
    return json.loads(raw)


async def _authenticate(ws: WebSocket) -> int | None:
    """Extract and validate the access token from query params. Closes the
    socket and returns None on any failure."""
    token = ws.query_params.get("token")
    if not token:
        await ws.close(code=1008)
        return None
    try:
        return decode_access_token(token)
    except Exception:
        await ws.close(code=1008)
        return None


async def _authorize_room(ws: WebSocket, room_id: str, user_id: int) -> dict | None:
    """Make sure the room exists and this user is actually a participant
    (i.e. their chat request was accepted) before we accept the socket."""
    try:
        room = await rpc_call(ConsumerQueue.CHAT_ROOM_GET, {"room_id": int(room_id), "user_id": user_id})
    except (ValueError, Exception):
        await ws.close(code=1008)
        return None
    if "error" in room:
        await ws.close(code=1008)
        return None
    return room


def _validate_content(msg: dict) -> str | None:
    """Return the validated content string, or None if invalid."""
    content = msg.get("content")
    if not isinstance(content, str) or not content.strip():
        return None
    if len(content) > MAX_CONTENT_LENGTH:
        return None
    return content


async def _persist_and_broadcast(ws: WebSocket, room_id: str, user_id: int, content: str) -> None:
    try:
        result = await rpc_call(
            ConsumerQueue.CHAT_MESSAGE_CREATE,
            {"room_id": int(room_id), "user_id": user_id, "content": content},
        )
    except Exception:
        logger.exception("Failed to persist chat message for room %s", room_id)
        await manager.send_local(ws, {"type": "error", "detail": "Failed to send message"})
        return

    if "error" in result:
        await manager.send_local(ws, {"type": "error", "detail": result["error"]})
        return

    # Broadcast the persisted record (real id/created_at) so every
    # client — including ones that reconnect later via REST — sees
    # the exact same message shape.
    await publish_room(room_id, {"type": "message", **result})


async def _handle_incoming_message(ws: WebSocket, room_id: str, user_id: int, msg: dict) -> None:
    msg_type = msg.get("type")

    if msg_type == "ping":
        await manager.send_local(ws, {"type": "pong"})
        return

    if msg_type != "message":
        await manager.send_local(ws, {"type": "error", "detail": "Unknown message type"})
        return

    content = _validate_content(msg)
    if content is None:
        await manager.send_local(
            ws, {"type": "error", "detail": "content must be a non-empty string, up to 4000 chars"}
        )
        return

    await _persist_and_broadcast(ws, room_id, user_id, content)


@router.websocket("/ws/rooms/{room_id}")
async def room_ws(ws: WebSocket, room_id: str):
    user_id = await _authenticate(ws)
    if user_id is None:
        return

    room = await _authorize_room(ws, room_id, user_id)
    if room is None:
        return

    await ws.accept()
    await manager.join(room_id, ws)
    sender_task = asyncio.create_task(manager.sender(ws))
    try:
        while True:
            try:
                msg = await ws.receive_json()
            except (json.JSONDecodeError, ValueError):
                await manager.send_local(ws, {"type": "error", "detail": "Invalid JSON"})
                continue
            await _handle_incoming_message(ws, room_id, user_id, msg)
    except WebSocketDisconnect:
        pass
    finally:
        sender_task.cancel()
        with suppress(asyncio.CancelledError):
            await sender_task
        await manager.leave(room_id, ws)
