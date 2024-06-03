#!/bin/sh

celery -A celery_tasks.tasks worker --loglevel=info &
python3 -m celery_tasks.entrypoint