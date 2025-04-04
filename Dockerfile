FROM python:3.13.2-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && pip install --no-cache-dir pipenv

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY Pipfile Pipfile.lock ./

RUN pipenv install --dev --deploy --ignore-pipfile --system

COPY . .