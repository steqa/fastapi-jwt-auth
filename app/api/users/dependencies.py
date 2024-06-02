from fastapi import Depends
from sqlalchemy.orm import Session

from api.database import get_db
from . import services, utils
from .exceptions import AuthError, UserInactive
from .models import User
from .schemas import UserLogin


def authenticate_user(
        user_data: UserLogin,
        db: Session = Depends(get_db)
) -> User:
    user = services.get_user_by_email(db, email=user_data.email)
    if not user:
        raise AuthError
    if not utils.validate_password(user_data.password, user.hashed_password):
        raise AuthError
    if not user.is_active:
        raise UserInactive
    return user
