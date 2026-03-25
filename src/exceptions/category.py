from fastapi import status

from src.exceptions.base import AppException


class CategoryNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "CATEGORY_NOT_FOUND"
    default_message = "Category not found or you don't have access to it"


class CategoryAlreadyExists(AppException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "CATEGORY_ALREADY_EXISTS"
    default_message = "Category with this name already exists"