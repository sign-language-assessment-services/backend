# Sign Language Assessment Services - Backend

This app is written in [Python][1] version 3.7 and uses the [FastAPI][2] framework.

## Prerequisites

The following software is required to use this app:

- [Python3.8][1]
- [pipenv][3] (package manager)
- [bash][4] if you want to use the `./go` script for build automation
  - **Windows**: there are several options to use bash, e.g.
    - [Git BASH](https://gitforwindows.org/)
    - [Windows Subsystem for Linux][6]
    - [Cygwin][7]
  - **MacOS**: bash is already pre-installed
  - **Linux**: In nearly all distributions, bash is already pre-installed

## Build automation: `./go`

All tasks related to building, testing, and running can be invoked with the `./go` script.
Run `./go` without any argument to see a list of all available tasks.

**NOTE**: You need _bash_ to run the `./go` script (see _Prerequisites_).
If you prefer to execute those tasks manually, you can use it as documentation.

### build: Install all libraries via Pipenv 

`./go build`

Install all libraries used by the app via pipenv. To understand what pipenv is doing under the
hood, please refer to the [pipenv documentation][3].

### test: Test the Fastapi web application (unit testing)

`./go test`

Launches all unit test files in `./test` folder via [pytest][8] which will be installed in the
build step using `./go build`. Pytest is configured via the file `pytest.ini`. 

### lint: Check how beautiful the code is written

`./go lint`

Checks if all Python files are written according to coding guidelines. This is done by using
 [pylint][9].

### run: Run the Fastapi web application in development mode, e.g. locally. 

`./go run`

Runs the app in development mode, i.e. starting a uvicorn server which allows requests to
`http://localhost:8000`. FastAPI also provides SwaggerUI which can be used interactively by
pointing a browser to `http://127.0.0.1:8000/docs`.

### image: Build a docker image

`./go image`

This requires that [Docker][11] is installed on your machine. Then this command will build a
docker image based on the given `Dockerfile` in the root folder of the repository.

### run-container: Run the docker image

`./go run-container`

Use this command if you have build your docker image via `./go image`. Then a container will
be started using these additional command line arguments:

  - `--rm`: Automatically remove the container when it exits
  - `-ti`: Allocate a pseudo-TTY and keep STDIN open even if not attached
  - `-p 80:80`: publish container's port 80 to the port 80 of the host machine
  - `--name "$IMAGE_TAG"`: Name the container for better monitoring

where `$IMAGE_TAG` refers to a name given in the `./go` script.

### run-compose: Start Fastapi app via `docker-compose` with all configured services

`./go run-compose`

If you want to start the whole network with all attached services encapsulated in Docker
files, then you can run the provided `docker-compose.yml` file, located in the root directory,
via `docker-compose` command. It requires that [Docker Compose][12] is installed. To see which
versions of Docker Engine and Docker Compose should be installed on your system, look at the
version number in the `docker-compose.yml` (e.g. `version: "3.5"`) file and compare it with the
[compatibility matrix in the Docker Compose documentation][13].

Note, that you have to stop the services manually afterwards. If you do not shut down the started
services, they will eventually be restarted for you again, even after a system reboot. You can
use the provided command `./go stop-compose` for that.

### stop-compose: Shut down all components (services and network) of the Fastapi web application

`./go stop-compose`

Shut down all services and networks configured in `docker-compose.yml`. This is necessary to
avoid unwanted restarts of services, even after the host machine was restarted. This is only
necessary if the Docker Compose file was started via `docker-compose -f docker-compose.yml` or
via `./go run-compose`, of course.  

### Precommit

`./go precommit`

This is a helpful command if you have changed something in the code and want to check if your
changes are okay for commiting and pushing them into the repository. Okay means that all tests
will pass and the linter gives you a perfect score, at least an acceptable one. Note, that this
command will not install the dev libraries. If you want to include these, you have to manually do
`./go build && ./go test && ./go lint` to have similar results. If any error occured after
running the command, you should consider not pushing your code changes into the repository, due
to the fact that it is very likely to have less robust code, then.

## Debug the app

For running the app in debug mode, you can best integrate it in an IDE and simply run
`application.py` in debug mode. It requires that the libraries are installed, i. e. `pipenv` is
working correctly. You can find out [more about debugging FastAPI in the tutorial][10].

## Learn more

- [Python][1] is one of the most loved and wanted programming languages (see https://insights.stackoverflow.com/survey/2019).
  Python tries to be as simple as possible for programmers. You can really write wonderful, beautiful code with Python.
- [FastAPI][2] has an excellent documentation and tries to keep things simple. It will also be a pleasure for you to work with FastAPI. It is also a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.


[1]: https://python.org
[2]: https://fastapi.tiangolo.com
[3]: https://github.com/pypa/pipenv
[4]: https://www.gnu.org/software/bash
[5]: https://gitforwindows.org
[6]: https://docs.microsoft.com/windows/wsl/install-win10
[7]: https://www.cygwin.com
[8]: https://docs.pytest.org
[9]: https://www.pylint.org
[10]: https://fastapi.tiangolo.com/tutorial/debugging
[11]: https://www.docker.com
[12]: https://docs.docker.com/compose/install
[13]: https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix
