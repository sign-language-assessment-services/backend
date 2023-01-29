FROM python:3.10-slim
MAINTAINER "Danny Rehl"

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
COPY ./.env /app/.env
COPY ./app /app/app

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction && yes | poetry cache clear --all .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
