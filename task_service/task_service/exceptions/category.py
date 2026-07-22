from shared.exceptions.base import AppException


class CategoryNotFoundError(AppException):
    status_code = 404
    error_code = "CATEGORY_NOT_FOUND"
    default_message = "Category not found"
