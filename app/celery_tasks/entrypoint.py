import redis

from .config import settings
from .handler import message_handler


def main():
    redis_conn = redis.Redis(
        host=settings.PUBSUB_REDIS_HOST,
        port=settings.REDIS_PORT
    )

    subscriber = redis_conn.pubsub()
    channels = ['schedule_delete_inactive_user', 'schedule_delete_email_confirm_code']
    for channel in channels:
        subscriber.subscribe(channel)

    for message in subscriber.listen():
        if message['type'] == 'message':
            message_handler(message)


if __name__ == '__main__':
    main()
