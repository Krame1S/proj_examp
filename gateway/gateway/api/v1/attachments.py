
import json
from typing import Annotated
 
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, status
 
from gateway.api.deps import get_current_user_id
from gateway.broker.rpc_publisher import rpc_publisher
from shared.contracts.attachment.contracts import AttachmentOut
from gateway.utils.s3 import delete_object, generate_key, get_public_url, upload_bytes
from shared.broker.queues import ConsumerQueue
 
router = APIRouter(prefix="/tasks/{task_id}/attachments", tags=["attachments"])
 
_MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB hard limit
 
 
@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    file: UploadFile,
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> AttachmentOut:
    """Receive a file, upload it to S3, then persist metadata via attachment_service."""
    data = await file.read()
    if len(data) > _MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large (max 20 MB).",
        )
 
    filename = file.filename or "upload"
    content_type = file.content_type or "application/octet-stream"
    key = generate_key(task_id, filename)
 
    # 1. Upload to S3 directly from the gateway
    try:
        await upload_bytes(key=key, data=data, content_type=content_type)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
 
    # 2. Persist metadata in attachment_service via RabbitMQ
    raw = await rpc_publisher.call(
        message=json.dumps(
            {
                "task_id": task_id,
                "owner_id": user_id,
                "key": key,
                "filename": filename,
                "content_type": content_type,
                "size": len(data),
            }
        ),
        request_queue_name=ConsumerQueue.ATTACHMENT_CREATE.value,
    )
 
    data_resp = json.loads(raw)
 
    if "error" in data_resp:
        # Roll back the S3 upload so we don't leave orphaned objects
        await delete_object(key)
        raise HTTPException(
            status_code=data_resp["error"]["status_code"],
            detail=data_resp["error"],
        )
 
    return AttachmentOut.model_validate(data_resp)
 
 
@router.get("", status_code=status.HTTP_200_OK)
async def list_attachments(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[AttachmentOut]:
    raw = await rpc_publisher.call(
        message=json.dumps({"task_id": task_id, "owner_id": user_id}),
        request_queue_name=ConsumerQueue.ATTACHMENT_LIST.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return [AttachmentOut.model_validate(item) for item in data]
 
 
@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    attachment_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    raw = await rpc_publisher.call(
        message=json.dumps(
            {
                "task_id": task_id,
                "attachment_id": attachment_id,
                "owner_id": user_id,
            }
        ),
        request_queue_name=ConsumerQueue.ATTACHMENT_DELETE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
 
