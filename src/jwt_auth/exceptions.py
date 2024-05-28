from fastapi import status
from src.exceptions import BaseHTTPException


class TokenInvalid(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token invalid'
