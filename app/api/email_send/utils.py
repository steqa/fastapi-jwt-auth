from datetime import datetime, UTC
from random import randint

from .exceptions import EmailConfirmCodeInvalid
from .models import EmailConfirmCode


def get_verification_code() -> int:
    return randint(100000, 999999)


def validate_email_confirm_code(
        expected_code: EmailConfirmCode,
        code: int
) -> EmailConfirmCode:
    now = datetime.now(UTC).replace(tzinfo=None)
    if (expected_code.code != code) or (now > expected_code.expired_at):
        raise EmailConfirmCodeInvalid

    return expected_code
