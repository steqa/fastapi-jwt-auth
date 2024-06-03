import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


class Settings:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT'))
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    PUBSUB_REDIS_HOST = os.getenv('PUBSUB_REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))

    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_FROM_NAME = os.getenv('EMAIL_FROM_NAME')
    EMAIL_FROM_ADDRESS = os.getenv('EMAIL_FROM_ADDRESS')


settings = Settings()
