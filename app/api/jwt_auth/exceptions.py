from fastapi import status

from api.exceptions import BaseHTTPException


class TokenInvalid(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token invalid'
