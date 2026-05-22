import json
from typing import Annotated
 
from fastapi import APIRouter, Body, HTTPException, status
 
from src.broker.rpc_publisher import rpc_publisher
from src.schemas.auth import SignUpRequest, TokenPair
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
 
    # user_service возвращает {"error": "..."} при бизнес-ошибках
    if "error" in data:
        error_code = data["error"]
        if error_code == "EMAIL_ALREADY_REGISTERED":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal service error",
        )
 
    return TokenPair.model_validate(data)




# @router.post("/sign-in")
# async def sign_in(payload: dict) -> dict:
#     pass

# @router.post("/refresh")
# async def refresh(payload: dict) -> dict:
#     pass

# @router.post("/sign-in")
# async def sign_in(
#     request: Annotated[SignInRequest, Body()],
#     auth_service: Annotated[AuthService, Depends(get_auth_service)],
# ) -> TokenPair:
#     return await auth_service.sign_in(request)


# @router.post("/refresh")
# async def refresh(
#     request: RefreshRequest,
#     auth_service: Annotated[AuthService, Depends(get_auth_service)],
# ) -> TokenPair:
#     return await auth_service.refresh(request.refresh_token)
