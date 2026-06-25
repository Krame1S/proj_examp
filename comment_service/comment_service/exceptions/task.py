from shared.exceptions.base import AppException


class TaskServiceError(AppException):
    pass


class TaskNotFound(TaskServiceError):
    status_code = 404
    error_code = "TASK_NOT_FOUND"
    default_message = "Task not found"
