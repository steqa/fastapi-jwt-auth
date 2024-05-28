import uuid

from sqlalchemy.orm import Session

from .models import User
from .schemas import UserCreate
from .utils import hash_password


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)
    del user.password_confirm
    del user.password
    user.email = user.email.lower()
    new_user = User(**user.model_dump(), hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session, skip: int, limit: int) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


def delete_user_by_id(db: Session, user_id: uuid.UUID) -> None:
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
