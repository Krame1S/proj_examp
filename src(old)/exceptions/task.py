from fastapi import status

from .base import AppException


class TaskNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "TASK_NOT_FOUND"
    default_message = "Task not found"
