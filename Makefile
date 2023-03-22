SHELL = /bin/sh

IMAGE_NAME:= slportal_backend
IMAGE_VERSION:= latest
IMAGE_TAG := ${IMAGE_NAME}:${IMAGE_VERSION}

REPOSITORY_FOLDER := ./
SERVER_PORT := 8000

.PHONY: default
default: help

.PHONY: all
all: install update lint test docker-build  ## install, update, lint, test and build docker image


.PHONY: clean
clean:	## delete caches, builds etc.
	rm -rf .mypy_cache
	rm -rf .pytest_cache pytest-results.xml

.PHONY: docker-build
docker-build:	## Build a docker image of this application
	docker build --rm -t ${IMAGE_TAG} ${REPOSITORY_FOLDER}

.PHONY: help
help:	## List targets and description
	@fgrep "##" $(lastword $(MAKEFILE_LIST)) | fgrep -v 'fgrep "##"' | sed 's/:.*##/:\n  /'

.PHONY: install
install:	## Install dependencies as configured in pyproject.toml
	poetry install

.PHONY: isort
isort:	## Check if imports are in the right order
	poetry run isort . --check --diff

.PHONY: lint
lint:	## Run linter
	poetry run isort . --check --diff
	poetry run pylint application.py app
	poetry run mypy --strict application.py app

.PHONY: run
run:	## Start a development server
	poetry run uvicorn app.main:app --port "${SERVER_PORT}" --reload

.PHONY: run-compose
run-compose:	## Boot up all docker services defined in docker-compose.yml
	docker-compose -f docker-compose.yml up -d

.PHONY: run-container
run-container:	## Start a dockerized development server
	docker run --rm -ti -p "${SERVER_PORT}":8000 --name "${IMAGE_NAME}" "${IMAGE_TAG}"

.PHONY: stop-compose
stop-compose:	## Stop the docker services gracefully
	docker-compose -f docker-compose.yml down

.PHONY: test
test:	## Run tests
	poetry run python -m pytest

.PHONY: update
update:	## Update application dependencies
	poetry update
