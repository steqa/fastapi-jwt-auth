from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    TIME_LOCALE: str
    # SITE_URL: str
    SITE_PORT: int

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int

    FLOWER_PORT: int

    JWT_PRIVATE_KEY_PATH: Path = BASE_DIR / 'certs/jwt-private.pem'
    JWT_PUBLIC_KEY_PATH: Path = BASE_DIR / 'certs/jwt-public.pem'
    JWT_ALGORITHM: str = 'RS256'

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    EMAIL_FROM_NAME: str
    EMAIL_FROM_ADDRESS: str

    EMAIL_CONFIRM_CODE_EXPIRE_MINUTES: int
    USER_CONFIRM_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=Path(BASE_DIR, '.env'))


settings = Settings()
