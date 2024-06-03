import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Settings:
    TIME_LOCALE = os.getenv('TIME_LOCALE')

    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT'))
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    PUBSUB_REDIS_HOST = os.getenv('PUBSUB_REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))

    JWT_PRIVATE_KEY_PATH = BASE_DIR / 'certs/jwt-private.pem'
    JWT_PUBLIC_KEY_PATH = BASE_DIR / 'certs/jwt-public.pem'
    JWT_ALGORITHM = 'RS256'

    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))

    EMAIL_CONFIRM_CODE_EXPIRE_MINUTES = int(os.getenv('EMAIL_CONFIRM_CODE_EXPIRE_MINUTES'))
    USER_CONFIRM_EXPIRE_MINUTES = int(os.getenv('USER_CONFIRM_EXPIRE_MINUTES'))


settings = Settings()
