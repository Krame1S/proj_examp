import json
from typing import Annotated
 
from fastapi import APIRouter, Body, HTTPException, status
 
from gateway.broker.rpc_publisher import rpc_publisher
from shared.contracts.auth.contracts import RefreshRequest, SignInRequest, SignUpRequest, TokenPair
from shared.broker.queues import ConsumerQueue


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up(
    request: Annotated[SignUpRequest, Body()],
) -> TokenPair:
    raw = await rpc_publisher.call(
        message=request.model_dump_json(),
        request_queue_name=ConsumerQueue.AUTH_SIGN_UP.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return TokenPair.model_validate(data)


@router.post("/sign-in", status_code=status.HTTP_200_OK)
async def sign_in(
    request: Annotated[SignInRequest, Body()],
) -> TokenPair:
    raw = await rpc_publisher.call(
        message=request.model_dump_json(),
        request_queue_name=ConsumerQueue.AUTH_SIGN_IN.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return TokenPair.model_validate(data)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    request: Annotated[RefreshRequest, Body()],
) -> TokenPair:
    raw = await rpc_publisher.call(
        message=request.model_dump_json(),
        request_queue_name=ConsumerQueue.AUTH_REFRESH.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return TokenPair.model_validate(data)