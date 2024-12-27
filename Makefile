SHELL = /bin/sh

IMAGE_NAME:= slportal_backend
IMAGE_VERSION:= latest
IMAGE_TAG := ${IMAGE_NAME}:${IMAGE_VERSION}

REPOSITORY_FOLDER := ./
SERVER_PORT := 8000

.PHONY: default
default: help

.PHONY: all
all: install update check docker-build	## install, update, lint, test and build docker image

.PHONY: check
check: lint test security	## Run all checks (linting, testing, security)

.PHONY: clean
clean:	## delete caches, builds etc.
	rm -rf .mypy_cache
	poetry run coverage erase || rm -rf .coverage
	find . -path ./.venv -prune -o -type f -name "pytest-results.xml" -print | xargs rm -f
	find . -path ./.venv -prune -o -type d -name ".pytest_cache" -print | xargs rm -rf
	find . -path ./.venv -prune -o -type d -name "__pycache__" -print | xargs rm -rf

.PHONY: coverage
MIN_COVERAGE ?= 95
coverage:	## Run test coverage
	poetry run coverage run -m pytest tests
	poetry run coverage report -m --fail-under=${MIN_COVERAGE}

coverage-codacy: SHELL:=/bin/bash
coverage-codacy:	## Send coverage report to codacy
	poetry run coverage xml -o cobertura.xml
	bash <(curl -Ls https://coverage.codacy.com/get.sh)

.PHONY: docker-build
docker-build:	## Build a docker image of this application
	docker build --rm -t ${IMAGE_TAG} ${REPOSITORY_FOLDER}

.PHONY: help
help:	## List targets and description
	@fgrep "##" $(lastword $(MAKEFILE_LIST)) | fgrep -v 'fgrep "##"' | sed 's/:.*##/:\n  /'

.PHONY: install
install:	## Install dependencies as configured in pyproject.toml
	poetry install --no-root

.PHONY: isort
isort:	## Check if imports are in the right order
	poetry run isort . --check --diff

.PHONY: lint
lint: isort pylint	## Run all linters

.PHONY: mypy
mypy:	## Run mypy in strict mode
	poetry run mypy --strict application.py app tests

.PHONY: pylint
pylint:	## Run pylint
	poetry run pylint application.py app
	poetry run pylint --disable=redefined-outer-name tests

.PHONY: pytest
pytest:	## Run tests
	poetry run python -m pytest tests

.PHONY: run
run:	## Start a development server
	docker-compose -f docker-compose.yml up -d database object-storage && poetry run uvicorn app.main:app --port "${SERVER_PORT}" --reload

.PHONY: run-compose
run-compose:	## Boot up all docker services defined in docker-compose.yml
	docker-compose -f docker-compose.yml up --build -d

.PHONY: run-container
run-container:	## Start a dockerized development server
	docker run --rm -ti -p "${SERVER_PORT}":8000 --name "${IMAGE_NAME}" "${IMAGE_TAG}"

.PHONY: security
security:	## Run security checks
	poetry run bandit -c pyproject.toml -r .

.PHONY: stop-compose
stop-compose:	## Stop the docker services gracefully
	docker-compose -f docker-compose.yml down

.PHONY: test
test: coverage	## Run all tests, including coverage

.PHONY: update
update:	## Update application dependencies
	poetry update
