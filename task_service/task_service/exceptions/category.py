from .base import AppException


class CategoryNotFound(AppException):
    status_code = 404
    error_code = "CATEGORY_NOT_FOUND"
    default_message = "Category not found"