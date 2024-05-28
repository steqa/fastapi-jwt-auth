from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.jwt_auth.dependencies import get_current_auth_user
from . import services
from .exceptions import (
    UserEmailExists,
)
from .pagination import Pagination
from .schemas import UserResponse, UserCreate

router = APIRouter(prefix='/api/v1/users', tags=['users'])


@router.post(
    '/',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise UserEmailExists
    user = services.create_user(db=db, user=user)
    return user


@router.get(
    '/',
    response_model=list[UserResponse],
)
def get_users(
        current_user: User = Depends(get_current_auth_user),
        pagination: Pagination = Depends(),
        db: Session = Depends(get_db)
):
    users = services.get_users(db, pagination.skip, pagination.limit)
    return users
