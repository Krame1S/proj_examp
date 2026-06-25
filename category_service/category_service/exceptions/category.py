from shared.exceptions.base import AppException


class CategoryServiceError(AppException):
    pass


class CategoryNotFoundError(CategoryServiceError):
    status_code = 404
    error_code = "CATEGORY_NOT_FOUND"
    default_message = "Category not found"


class CategoryAlreadyExistsError(CategoryServiceError):
    status_code = 409
    error_code = "CATEGORY_ALREADY_EXISTS"
    default_message = "Category with this name already exists"
