from uuid import UUID

from celery import Celery
from sqlalchemy.orm import sessionmaker, Session

from src.config import settings
from src.database import engine
from src.users import services as users_service

celery = Celery(
    'tasks',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0',
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def with_db_session(func):
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            return func(db, *args, **kwargs)
        finally:
            db.close()

    return wrapper


@celery.task(name='delete_inactive_user')
@with_db_session
def __delete_inactive_user(db: Session, user_id: str):
    user_id = UUID(user_id)
    user = users_service.get_user_by_id(db, user_id)
    if user and not user.is_active:
        users_service.delete_user_by_id(db, user_id)


def schedule_delete_inactive_user(
        user_id: UUID,
        delay: int = settings.USER_CONFIRM_EXPIRE_MINUTES
):
    __delete_inactive_user.apply_async(args=[str(user_id)], countdown=delay * 60)