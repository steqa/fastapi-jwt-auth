FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "-m", "email_sender.entrypoint"]