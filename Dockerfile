FROM python:3.13-alpine
LABEL authors="Helmut"

RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-root

COPY . .



