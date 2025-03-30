FROM python:3.13-slim

WORKDIR /app

RUN apt update && apt install -y curl
RUN pip install poetry==2.1.2 && poetry config virtualenvs.create false

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
COPY ./alembic.ini /app/alembic.ini
COPY ./db_migrations /app/db_migrations

RUN poetry install --no-interaction --no-root && yes | poetry cache clear --all .

COPY ./app /app/app
COPY ./logging.yaml /app/logging.yaml

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging.yaml"]
