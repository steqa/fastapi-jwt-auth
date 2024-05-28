from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from src.database import get_db
from src.jwt_auth.utils import REFRESH_TOKEN_TYPE
from src.users import services
from src.users.models import User
from .exceptions import TokenInvalid
from .utils import decode_jwt

http_bearer = HTTPBearer()


def get_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    try:
        token = credentials.credentials
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise TokenInvalid
    return payload


def get_current_auth_user_for_refresh(
        token_payload: dict = Depends(get_token_payload),
        db: Session = Depends(get_db),
) -> User:
    validate_token_type(token_payload, REFRESH_TOKEN_TYPE)
    return get_user_by_token_sub(token_payload, db)


def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get('type') == token_type:
        return True
    else:
        raise TokenInvalid


def get_user_by_token_sub(payload: dict, db) -> User:
    user_email = payload.get('sub')
    user = services.get_user_by_email(db, email=user_email)
    if not user:
        raise TokenInvalid
    return user
