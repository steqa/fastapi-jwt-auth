import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.jwt_auth.dependencies import get_current_auth_user
from src.users.exceptions import UserNotFound, NotAuthenticated
from src.users.models import User
from src.users.services import get_user_by_id
from . import services
from .exceptions import EmailConfirmCodeExists
from .schemas import EmailConfirmCodeResponse
from .utils import send_registration_confirm_email

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