FROM python:3.10-slim

MAINTAINER "Danny Rehl <commit-connoisseur@posteo.de>"

WORKDIR /app

RUN apt update && apt install -y curl
RUN pip install poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
RUN poetry install --no-interaction && yes | poetry cache clear --all .

COPY ./app /app/app
COPY ./.env /app/.env
COPY ./logging.yaml /app/logging.yaml

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging.yaml"]
