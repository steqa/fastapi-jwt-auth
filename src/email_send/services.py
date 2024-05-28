import uuid

from sqlalchemy.orm import Session

from .models import EmailConfirmCode
from .utils import get_verification_code


def create_email_confirm_code(db: Session, user_id: uuid.UUID) -> EmailConfirmCode:
    code = get_verification_code()
    new_code = EmailConfirmCode(user_id=user_id, code=code)
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code