import json
from datetime import datetime

from .tasks import (
    schedule_delete_inactive_user,
    schedule_delete_email_confirm_code
)


def message_handler(message):
    channel = message['channel'].decode('utf-8')
    data = message['data'].decode('utf-8')
    data = json.loads(data)
    if channel == 'schedule_delete_inactive_user':
        schedule_delete_inactive_user(
            user_id=data['user_id'],
            delay_seconds=int(data['delay_seconds'])
        )
    elif channel == 'schedule_delete_email_confirm_code':
        schedule_delete_email_confirm_code(
            code_id=data['code_id'],
            delete_at=datetime.strptime(data['delete_at'], '%Y-%m-%d %H:%M:%S')
        )
