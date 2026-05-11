from typing import Annotated

from fastapi import APIRouter, Depends, File, Path, UploadFile, status

from src.api.deps import get_attachment_service, get_current_user_id
from src.schemas.attachment import AttachmentOut
from src.service.attachment import AttachmentService
from fastapi import HTTPException


router = APIRouter(prefix="/tasks/{task_id}/attachments", tags=["attachments"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    attachment_service: Annotated[AttachmentService, Depends(get_attachment_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    file: Annotated[UploadFile, File()],
) -> AttachmentOut:
    data = await file.read()

    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large, max 10MB")

    return await attachment_service.upload_attachment(
        task_id=task_id,
        owner_id=current_user_id,
        filename=file.filename or "unknown",
        content_type=file.content_type or "application/octet-stream",
        data=data,
    )


@router.get("", status_code=status.HTTP_200_OK)
async def list_attachments(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    attachment_service: Annotated[AttachmentService, Depends(get_attachment_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[AttachmentOut]:
    return await attachment_service.list_attachments(task_id, current_user_id)


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    attachment_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    attachment_service: Annotated[AttachmentService, Depends(get_attachment_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    await attachment_service.delete_attachment(attachment_id, current_user_id)