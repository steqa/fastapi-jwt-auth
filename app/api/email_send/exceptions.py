from fastapi import status

from api.exceptions import BaseValidationError, BaseHTTPException


class EmailConfirmCodeInvalid(BaseValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    field = 'code'
    message = 'Code invalid'


class EmailConfirmCodeExists(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Code already exists for this user'


class UserAlreadyActivated(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User already activated'
