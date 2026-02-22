FROM python:3.13-alpine
LABEL authors="Helmut"

WORKDIR /code

RUN pip install poetry

COPY . .



