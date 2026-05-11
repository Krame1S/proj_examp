from fastapi import status
from src.exceptions.base import AppException


class AttachmentNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "ATTACHMENT_NOT_FOUND"
    default_message = "Attachment not found"


class AttachmentUploadFailed(AppException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "ATTACHMENT_UPLOAD_FAILED"
    default_message = "File upload failed, please try again later"