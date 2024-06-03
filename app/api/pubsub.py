import json
from datetime import datetime
from uuid import UUID

from redis import Redis

from api.config import settings

redis_conn = Redis(host='pubsub_redis', port=6379, db=0)


def __publish_message(chanel: str, message: str):
    redis_conn.publish(chanel, message)


def __send_email(email_type: str, to: str, code: int, expired_at: datetime):
    message = json.dumps({
        'email_type': email_type,
        'to': to,
        'code': code,
        'expired_at': expired_at.strftime('%Y-%m-%d %H:%M:%S')
    })
    __publish_message('send_email', message)


def send_registration_confirm_email(to: str, code: int, expired_at: datetime):
    __send_email('registration_confirm', to, code, expired_at)


def schedule_delete_inactive_user(
        user_id: UUID,
        delay_seconds: int | None = settings.USER_CONFIRM_EXPIRE_MINUTES * 60
):
    message = json.dumps({
        'user_id': str(user_id),
        'delay_seconds': delay_seconds
    })
    __publish_message('schedule_delete_inactive_user', message)


def schedule_delete_email_confirm_code(code_id: UUID, delete_at: datetime):
    message = json.dumps({
        'code_id': str(code_id),
        'delete_at': delete_at.strftime('%Y-%m-%d %H:%M:%S')
    })
    __publish_message('schedule_delete_email_confirm_code', message)
