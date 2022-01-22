FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update

# Install packages
RUN apt-get install -y \
  libpq-dev \
  python3-psycopg2 \
  python3-dev \
  gcc

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN pip install --ignore-installed poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction
