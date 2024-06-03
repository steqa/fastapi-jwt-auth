from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = automap_base()

Base.prepare(engine, reflect=True)

User = Base.classes.users
EmailConfirmCode = Base.classes.email_confirm_code
