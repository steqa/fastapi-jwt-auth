from fastapi import status
from fastapi.exceptions import HTTPException, RequestValidationError


class BaseValidationError(RequestValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    field = message = type = 'string'
    error_type = 'value_error'

    def __init__(self):
        super().__init__(self.errors())

    @classmethod
    def errors(cls) -> dict:
        return {
            'loc': ['body', cls.field],
            'msg': cls.message,
            'type': cls.type
        }


class MultiValidationError(RequestValidationError):
    def __init__(self, error_classes, status_code: int):
        self.status_code = status_code
        errors = [error.errors() for error in error_classes]
        super().__init__(errors)


class BaseHTTPException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Bad Request'

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )

    @classmethod
    def response_example(cls) -> tuple[int, dict]:
        return (
            cls.status_code, {
                'content': {'application/json': {'example': {
                    'detail': cls.detail
                }}}
            }
        )
