FROM python:3.13.2-slim AS builder

RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
    build-essential \
    && pip install --no-cache-dir pipenv

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY Pipfile Pipfile.lock ./

RUN pipenv install --dev --deploy --ignore-pipfile --system

FROM python:3.13.2-slim

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY pyproject.toml setup.cfg Makefile ./
COPY src /app