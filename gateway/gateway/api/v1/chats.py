import json
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from shared.broker.queues import ConsumerQueue
from shared.contracts.chats.contracts import ChatRequestOut, GetMessagesResponse

from gateway.api.deps import get_current_user_id
from gateway.broker.rpc_publisher import rpc_publisher

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/requests", status_code=status.HTTP_201_CREATED)
async def create_request(
    email: Annotated[str, Body(embed=True)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> ChatRequestOut:
    raw = await rpc_publisher.call(
        message=json.dumps({"email": email, "user_id": user_id}),
        request_queue_name=ConsumerQueue.CHAT_REQUEST_CREATE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return ChatRequestOut.model_validate(data)


@router.get("/requests", status_code=status.HTTP_200_OK)
async def list_requests(
    direction: Annotated[str, Query(pattern="^(incoming|outgoing)$")],
    user_id: Annotated[int, Depends(get_current_user_id)],
    status: Annotated[str | None, Query(pattern="^(pending|accepted|declined|cancelled)$")] = None,
) -> list[ChatRequestOut]:
    raw = await rpc_publisher.call(
        message=json.dumps({"user_id": user_id, "direction": direction, "status": status}),
        request_queue_name=ConsumerQueue.CHAT_REQUEST_LIST.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return [ChatRequestOut.model_validate(r) for r in data]


@router.post("/requests/{request_id}/accept", status_code=status.HTTP_200_OK)
async def accept_request(
    request_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> ChatRequestOut:
    raw = await rpc_publisher.call(
        message=json.dumps({"request_id": request_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.CHAT_REQUEST_ACCEPT.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return ChatRequestOut.model_validate(data)


@router.post("/requests/{request_id}/decline", status_code=status.HTTP_200_OK)
async def decline_request(
    request_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> ChatRequestOut:
    raw = await rpc_publisher.call(
        message=json.dumps({"request_id": request_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.CHAT_REQUEST_DECLINE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return ChatRequestOut.model_validate(data)


@router.post("/requests/{request_id}/cancel", status_code=status.HTTP_200_OK)
async def cancel_request(
    request_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> ChatRequestOut:
    raw = await rpc_publisher.call(
        message=json.dumps({"request_id": request_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.CHAT_REQUEST_CANCEL.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return ChatRequestOut.model_validate(data)


@router.get("/rooms", status_code=status.HTTP_200_OK)
async def list_rooms(
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[ChatRequestOut]:
    raw = await rpc_publisher.call(
        message=json.dumps({"user_id": user_id}),
        request_queue_name=ConsumerQueue.CHAT_ROOM_LIST.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return [ChatRequestOut.model_validate(r) for r in data]


@router.get("/rooms/{room_id}/messages", status_code=status.HTTP_200_OK)
async def list_messages(
    room_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    before_id: Annotated[int | None, Query(ge=1)] = None,
) -> GetMessagesResponse:
    raw = await rpc_publisher.call(
        message=json.dumps({"room_id": room_id, "user_id": user_id, "limit": limit, "before_id": before_id}),
        request_queue_name=ConsumerQueue.CHAT_MESSAGE_LIST.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return GetMessagesResponse.model_validate(data)
