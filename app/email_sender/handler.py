import json
from datetime import datetime

from .utils import send_registration_confirm_email


def message_handler(message):
    channel = message['channel'].decode('utf-8')
    data = message['data'].decode('utf-8')
    data = json.loads(data)
    if channel == 'send_email':
        if data['email_type'] == 'registration_confirm':
            send_registration_confirm_email(
                to=data['to'],
                code=data['code'],
                expired_at=datetime.strptime(data['expired_at'], '%Y-%m-%d %H:%M:%S')
            )
