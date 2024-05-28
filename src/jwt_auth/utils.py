from datetime import timedelta, datetime, UTC

import jwt
from src.config import settings


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
