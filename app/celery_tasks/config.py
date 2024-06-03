import os


class Settings:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT'))
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    PUBSUB_REDIS_HOST = os.getenv('PUBSUB_REDIS_HOST')
    CELERY_REDIS_HOST = os.getenv('CELERY_REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))


settings = Settings()
