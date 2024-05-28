from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    JWT_PRIVATE_KEY_PATH: Path = BASE_DIR / 'certs/jwt-private.pem'
    JWT_PUBLIC_KEY_PATH: Path = BASE_DIR / 'certs/jwt-public.pem'
    JWT_ALGORITHM: str = 'RS256'

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(env_file=Path(BASE_DIR, '.env'))


settings = Settings()
