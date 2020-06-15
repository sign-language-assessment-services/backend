#!/usr/bin/env bash

# This script contains all tasks related to building, testing and running the application

## Adding a new task:
# 1. To add a task named 'example', implement it as a function named 'goal_example()'
# 2. Above the function name, add a usage hint, e.g. '##DOC: example: this is an example'
#    -> Usage hints will be displayed when running this script without any argument or with an unknown argument
# 3. The task can now be invoked with `./go example`


## Tasks  ================================================================================

##DOC build: build the application (i.e. install libraries)
goal_build() {
  pipenv install
}

##DOC test: execute all tests (i.e. running pytest)
goal_test() {
  pipenv run pytest
}

##DOC lint: lint all code files (i.e. running pylint)
goal_lint() {
  pipenv run pylint app/ test/
}

##DOC run: run the application (i.e. starting uvicorn)
goal_run() {
  pipenv run uvicorn app.main:app --reload
}

##DOC all: build, test, lint and run application (breaks on errors)
goal_all() {
  goal_build && \
  goal_test  && \
  goal_lint  && \
  goal_run
}

## ========================================================================================

## Include go.helpers script which invokes specified task or prints usage hint
DIR_NAME="$(dirname "$0")"
source "$DIR_NAME/go.helpers"
