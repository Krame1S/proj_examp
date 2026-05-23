from fastapi import APIRouter, Body, Depends, HTTPException, status
import json
from typing import Annotated
from fastapi import APIRouter, Body, Depends, status
from src.api.deps import get_current_user_id
from src.broker.rpc_publisher import rpc_publisher
from src.schemas.user import UserProfile, UserUpdate
from shared.broker.queues import ConsumerQueue

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_profile(
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> UserProfile:
    raw = await rpc_publisher.call(
        message=json.dumps({"user_id": user_id}),
        request_queue_name=ConsumerQueue.USER_GET_PROFILE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return UserProfile.model_validate(data)


@router.put("/me")
async def update_profile(
    body: Annotated[UserUpdate, Body()],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> UserProfile:
    raw = await rpc_publisher.call(
        message=json.dumps({"user_id": user_id, "email": body.email}),
        request_queue_name=ConsumerQueue.USER_UPDATE_PROFILE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return UserProfile.model_validate(data)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    raw = await rpc_publisher.call(
        message=json.dumps({"user_id": user_id}),
        request_queue_name=ConsumerQueue.USER_DELETE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )