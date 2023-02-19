FROM python:3.10-slim
MAINTAINER "Danny Rehl"

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
COPY ./.env /app/.env
COPY ./app /app/app
COPY logging.yaml /app

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction && yes | poetry cache clear --all .
RUN apt update && apt install -y curl

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging.yaml"]
