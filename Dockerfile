FROM python:3.13-alpine
LABEL authors="Helmut"

#RUN apk add --no-cache \
#    postgresql-client \
#    postgresql-dev \
#    gcc \
#    musl-dev \
#    libffi-dev \
#    jpeg-dev \
#    zlib-dev \
RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-root

COPY . .

RUN mkdir -p staticfiles media

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]





