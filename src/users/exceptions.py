from fastapi import status
from src.exceptions import BaseValidationError, BaseHTTPException


class UserEmailExists(BaseValidationError):
    status_code = status.HTTP_409_CONFLICT
    field = 'email'
    message = 'Email already registered'


class AuthError(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid email or password'


class UserInactive(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'User inactive'


class UserNotFound(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'User not found'


class NotAuthenticated(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Not authenticated'
