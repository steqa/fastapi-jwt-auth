import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.jwt_auth.dependencies import get_current_auth_user
from api.users.exceptions import UserNotFound, NotAuthenticated
from api.users.models import User
from api.users.schemas import UserResponse
from api.users.services import get_user_by_id, activate_user
from . import services
from .exceptions import EmailConfirmCodeExists, UserAlreadyActivated
from .schemas import EmailConfirmCodeResponse
from .utils import send_registration_confirm_email, validate_email_confirm_code

router = APIRouter(prefix='/api/v1/email', tags=['email'])


@router.post(
    '/create-email-confirm-code',
    response_model=EmailConfirmCodeResponse,
    status_code=status.HTTP_201_CREATED,
    responses=dict([
        NotAuthenticated.response_example(),
        UserNotFound.response_example(),
        EmailConfirmCodeExists.response_example()
    ])
)
def create_email_confirm_code(
        user_id: uuid.UUID,
        current_user: User = Depends(get_current_auth_user),
        db: Session = Depends(get_db)
):
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise UserNotFound

    code = services.get_email_confirm_code_by_user_id(db=db, user_id=user_id)
    if code:
        raise EmailConfirmCodeExists

    code = services.create_email_confirm_code(db=db, user_id=user_id)
    send_registration_confirm_email(to=user.email, code=code)
    return code


@router.post(
    '/confirm-email',
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses=dict([
        UserNotFound.response_example(),
        UserAlreadyActivated.response_example()
    ])
)
def confirm_email(user_id: uuid.UUID, code: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise UserNotFound
    if user.is_active:
        raise UserAlreadyActivated

    expected_code = services.get_email_confirm_code_by_user_id(db=db, user_id=user_id)
    if not expected_code:
        raise UserNotFound
    validate_email_confirm_code(expected_code, code)
    user = activate_user(db=db, user_id=user_id)
    services.delete_email_confirm_code_by_id(db=db, code_id=expected_code.id)
    return user
