import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import settings, TEMPLATES


def __send_email(
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
        email_html = TEMPLATES.get_template(html_template).render(context)
        msg.attach(MIMEText(email_html, 'html'))

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(msg)


def send_registration_confirm_email(
        to: str,
        code: int,
        expired_at: datetime,
):
    subject = 'Подтверждение регистрации.'
    template = 'registration_confirm.html'
    context = {'code': code, 'expired_at': expired_at}
    __send_email(to=to, subject=subject, html_template=template, context=context)
