from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()


@app.exception_handler(RequestValidationError)
def handle_validation_error(
        request: Request,
        exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    if type(errors) is dict:
        errors = [errors]

    status_code = getattr(exc, 'status_code',
                          status.HTTP_422_UNPROCESSABLE_ENTITY)
    detail = []
    for error in errors:
        er_loc = error['loc']
        er_msg = error['msg'].lstrip('Value error, ')
        er_type = error['type']
        detail.append({'loc': er_loc, 'msg': er_msg, 'type': er_type})
    return JSONResponse(status_code=status_code, content={'detail': detail})
