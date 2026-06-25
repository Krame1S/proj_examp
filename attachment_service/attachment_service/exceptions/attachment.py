from shared.exceptions.base import AppException

class AttachmentServiceError(AppException):
    pass

class AttachmentNotFound(AppException):
    status_code = 404
    error_code = "ATTACHMENT_NOT_FOUND"
    default_message = "Attachment not found"


class AttachmentUploadFailed(AppException):
    status_code = 503
    error_code = "ATTACHMENT_UPLOAD_FAILED"
    default_message = "File upload failed, please try again later"