import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.email_send.routers import create_email_confirm_code
from src.jwt_auth.dependencies import get_current_auth_user
from src.jwt_auth.exceptions import TokenInvalid
from . import services
from .exceptions import (
    NotAuthenticated,
    UserEmailExists,
    UserNotFound,
)
from .models import User
from .pagination import Pagination
from .schemas import UserResponse, UserCreate
from src.celery_tasks import tasks

router = APIRouter(prefix='/api/v1/users', tags=['users'])


@router.post(
    '/',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses=dict([TokenInvalid.response_example()])
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise UserEmailExists
    user = services.create_user(db=db, user=user)
    code = create_email_confirm_code(user_id=user.id, db=db)
    tasks.schedule_delete_inactive_user(user_id=user.id)
    tasks.schedule_delete_email_confirm_code(
        code_id=code.id, delete_at=code.expired_at
    )
    return user


@router.get(
    '/',
    response_model=list[UserResponse],
    responses=dict([
        NotAuthenticated.response_example(),
        TokenInvalid.response_example()
    ])
)
def get_users(
        current_user: User = Depends(get_current_auth_user),
        pagination: Pagination = Depends(),
        db: Session = Depends(get_db)
):
    users = services.get_users(db, pagination.skip, pagination.limit)
    return users


@router.get(
    '/me/',
    response_model=UserResponse,
    responses=dict([
        NotAuthenticated.response_example(),
        TokenInvalid.response_example()
    ])
)
def get_current_user(current_user: User = Depends(get_current_auth_user)):
    return current_user


@router.get(
    '/{user_uuid}/',
    response_model=UserResponse,
    responses=dict([
        NotAuthenticated.response_example(),
        TokenInvalid.response_example(),
        UserNotFound.response_example()
    ])
)
def get_user(
        user_id: uuid.UUID,
        current_user: User = Depends(get_current_auth_user),
        db: Session = Depends(get_db)
):
    user = services.get_user_by_id(db, user_id=user_id)
    if not user:
        raise UserNotFound
    return user
