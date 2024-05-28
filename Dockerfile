FROM python:3.12

RUN apt-get update && apt-get install -y locales locales-all

WORKDIR /app

COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN chmod a+x docker/*.sh
