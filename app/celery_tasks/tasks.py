from datetime import datetime
from uuid import UUID

from celery import Celery
from sqlalchemy.orm import sessionmaker, Session

from .config import settings
from .database import engine, User, EmailConfirmCode

celery = Celery(
    'tasks',
    broker=f'redis://{settings.CELERY_REDIS_HOST}:{settings.REDIS_PORT}/0',
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


@celery.task(name='schedule_delete_user')
@with_db_session
def __delete_inactive_user(db: Session, user_id: str):
    user_id = UUID(user_id)
    user = db.query(User).filter(User.id == user_id).first()
    if user and not user.is_active:
        db.query(User).filter(User.id == user_id).delete()
        db.commit()


@celery.task(name='delete_email_confirm_code')
@with_db_session
def __delete_email_confirm_code(db: Session, code_id: str):
    code_id = UUID(code_id)
    code = db.query(EmailConfirmCode).filter(EmailConfirmCode.id == code_id).first()
    if code:
        db.query(EmailConfirmCode).filter(EmailConfirmCode.id == code_id).delete()
        db.commit()


def schedule_delete_inactive_user(
        user_id: str,
        delay_seconds: int
):
    __delete_inactive_user.apply_async(args=[user_id], countdown=delay_seconds)


def schedule_delete_email_confirm_code(
        code_id: str,
        delete_at: datetime
):
    __delete_email_confirm_code.apply_async(args=[code_id], eta=delete_at)
