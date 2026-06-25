import logging
import os

from aiobotocore.session import get_session
from botocore.exceptions import ClientError, EndpointConnectionError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from attachment_service.core.config import settings

logger = logging.getLogger(__name__)

# ==================== MOCK MODE ====================
MOCK_S3 = settings.DEBUG or os.getenv("MOCK_S3", "false").lower() in ("true", "1", "yes")


_s3_retry = retry(
    retry=retry_if_exception_type((ClientError, EndpointConnectionError, OSError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before_sleep=lambda rs: logger.warning(
        "S3 retry attempt %s after: %s",
        rs.attempt_number,
        rs.outcome.exception() if rs.outcome else "unknown",
    ),
)


def _get_s3_client():
    session = get_session()
    return session.create_client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL or None,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION,
    )


def get_public_url(key: str) -> str:
    if MOCK_S3:
        return f"http://mock-s3.local/files/{key}"
    return f"{settings.S3_PUBLIC_URL.rstrip('/')}/{key}"


@_s3_retry
async def delete_object(key: str) -> None:
    """Delete an object from S3. In mock mode just logs."""
    if MOCK_S3:
        logger.info("🟡 [MOCK S3] delete → %s", key)
        return

    async with _get_s3_client() as client:
        await client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=key)
    logger.info("Deleted %s", key)