import logging

import aiohttp
from aiobotocore.session import get_session
from botocore.exceptions import ClientError, EndpointConnectionError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from src.core.config import settings

logger = logging.getLogger(__name__)

_s3_retry = retry(
    retry=retry_if_exception_type((ClientError, EndpointConnectionError, OSError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before_sleep=lambda rs: logger.warning("S3 retry attempt %s after %s", rs.attempt_number, rs.outcome.exception() if rs.outcome else "unknown"),
)


def _get_s3_client():
    session = get_session()
    return session.create_client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION,
    )


@_s3_retry
async def upload_bytes(key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
    async with _get_s3_client() as client:
        await client.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=key,
            Body=data,
            ContentType=content_type,
        )
    logger.info("Uploaded %s (%d bytes)", key, len(data))


@_s3_retry
async def upload_from_url(key: str, url: str, content_type: str = "application/octet-stream") -> str | None:
    async with aiohttp.ClientSession() as http, http.get(url) as resp:
        if resp.status != 200:
            logger.error("Failed to download from %s: HTTP %d", url, resp.status)
            return None
        data = await resp.read()

    await upload_bytes(key, data, content_type)
    return get_public_url(key)


@_s3_retry
async def delete_object(key: str) -> None:
    async with _get_s3_client() as client:
        await client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=key)
    logger.info("Deleted %s", key)


def get_public_url(key: str) -> str:
    return f"{settings.S3_PUBLIC_URL}/{key}"
