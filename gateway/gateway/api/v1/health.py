from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str = "ok"


@router.get("")
async def health() -> HealthResponse:
    return HealthResponse()
