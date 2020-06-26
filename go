#!/usr/bin/env bash

# This script contains all tasks related to building, testing and
# running the application.

## How to add a new task ===============================================

# 1. To add a task named 'example', implement it as a function named
#    'goal_example()'.
# 2. Add a usage hint above the function name, which will be displayed
#    when running this script without any argument or without an unknown
#    argument , e.g.: `##DOC: example: this is an example`.
# 3. The task can now be invoked with `./go example`

## Global variables ====================================================

REPO_DIR=$(dirname "$0")  # The base directory of this repository
IMAGE_TAG="slportal_backend"  # Image tag used by docker build

## Tasks  ==============================================================

##DOC build: Build the application, i.e. install libraries.
goal_build() {
  pipenv install --dev
}

##DOC test: Execute all tests, i.e. running pytest.
goal_test() {
  pipenv run pytest
}

##DOC lint: Lint all code files, i.e. running pylint.
goal_lint() {
  pipenv run pylint application.py app/ test/
}

##DOC run: Run the application, i.e. starting uvicorn.
goal_run() {
  # This will run the application on a local machine via uvicorn server.
  # It requires that the app was built before, e.g. via `./go build`.
  pipenv run uvicorn app.main:app --reload
}

##DOC image: Build docker image using the provided Dockerfile.
goal_image() {
  docker build -t "$IMAGE_TAG" "$REPO_DIR"
}

##DOC run-container: Run the docker container build via `./go image`.
goal_run-container() {
  docker run --rm -ti -p 80:80 --name "$IMAGE_TAG" "$IMAGE_TAG"
}

##DOC run-compose: Get web api running through docker-compose.
goal_run-compose() {
  # `docker-compose` will start all configured services from the file
  # `docker-compose.yml`.  They will also (re)build if necessary.  Note
  # that the services has to be stopped via `./go stop-compose` to avoid
  # service restarts, even after a system reboot.
  docker-compose -f "$REPO_DIR/docker-compose.yml" up -d
}

##DOC run-compose: Get web api running through docker-compose.
goal_stop-compose() {
  # `docker-compose` will restart the app if possible, even after a
  # system reboot.  You have to explicitely stop the docker services.
  docker-compose -f "$REPO_DIR/docker-compose.yml" down
}

##DOC precommit: Build, test and lint code before committing/pushing it.
goal_precommit() {
  pipenv install && \
  goal_test  && \
  goal_lint
}

## =====================================================================

## Include `go.helpers` for getting task running or printing usage hint.
DIR_NAME="$(dirname "$0")"
source "$DIR_NAME/go.helpers"
