from datetime import timedelta, datetime, UTC

import jwt

from api.config import settings

ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


def create_access_token(user):
    jwt_payload = {
        'type': ACCESS_TOKEN_TYPE,
        'sub': user.email,
        'email': user.email,
    }
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(user):
    jwt_payload = {
        'type': REFRESH_TOKEN_TYPE,
        'sub': user.email,
    }
    return encode_jwt(
        payload=jwt_payload,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def encode_jwt(
        payload: dict,
        private_key: str = settings.JWT_PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.JWT_ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.JWT_PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.JWT_ALGORITHM,
) -> dict:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded
