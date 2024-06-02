import smtplib
from datetime import datetime, UTC
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from random import randint

from fastapi.templating import Jinja2Templates

from api.config import settings
from .exceptions import EmailConfirmCodeInvalid
from .models import EmailConfirmCode

TEMPLATES_DIR = Path(__file__).parent / 'templates'
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def get_verification_code() -> int:
    return randint(100000, 999999)


def send_email(
        to: str,
        subject: str,
        plain_text: str | None = None,
        html_template: str | None = None,
        context: dict | None = None
):
    msg = MIMEMultipart()
    msg['From'] = f'{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM_ADDRESS}>'
    msg['To'] = to
    msg['Subject'] = subject
    if plain_text:
        msg.attach(MIMEText(plain_text, 'plain'))
    if html_template:
        if not context:
            context = {}
        email_html = templates.get_template(html_template).render(context)
        msg.attach(MIMEText(email_html, 'html'))

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(msg)


def send_registration_confirm_email(
        to: str,
        code: EmailConfirmCode,
):
    subject = 'Подтверждение регистрации.'
    template = 'registration_confirm.html'
    context = {'code': code.code, 'expired_at': code.expired_at}
    send_email(to=to, subject=subject, html_template=template, context=context)


def validate_email_confirm_code(
        expected_code: EmailConfirmCode,
        code: int
) -> EmailConfirmCode:
    now = datetime.now(UTC).replace(tzinfo=None)
    if (expected_code.code != code) or (now > expected_code.expired_at):
        raise EmailConfirmCodeInvalid

    return expected_code
