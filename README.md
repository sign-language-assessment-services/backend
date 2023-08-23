[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/eb0c22856be54da29d31f373e39dfa8a)](https://app.codacy.com/gh/sign-language-assessment-services/backend/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/eb0c22856be54da29d31f373e39dfa8a)](https://app.codacy.com/gh/sign-language-assessment-services/backend/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

# Sign Language Assessment Services - Backend

This is a web application realized as REST-API using [Python][1] and the
[FastAPI][2] framework. It provides the functionality necessary to provide
a portal where sign languages can be learned.

## Prerequisites

The following software is required to use this app:

- [Python3.10][1] or a higher version

## Build automation: `Makefile`

All tasks related to building, testing, and running can be invoked with make
commands. Run `make help` to see a list of all available tasks.

**NOTE**: If you prefer to perform certain tasks manually, the content of the
file is probably interesting for you, e.g. if you want to run the server on a
different port or name the docker container differently.

### install: Install all libraries via Poetry 

`make install`

Installs all libraries used by the app via Poetry. To understand what Poetry
is, please look into the [poetry documentation][3].

### test: Test the Fastapi web application (unit testing)

`make test`

Launches [Pytest][8]'s test runner, which will collect all unit test files in
the `./test` folder. It will be installed in the install step using
`make install`. Pytest configuration is done in the `pyproject.toml` file.

### lint: Check how beautiful the code is written

`make lint`

Checks if all Python files are written according to coding guidelines. This is
done by using [Pylint][9]. Pylint configuration is done in the `pyproject.toml`
file.

### run: Run the Fastapi web application in development mode 

`make run`

Runs the app in development mode, i.e. starting a uvicorn server which allows
requests to `http://127.0.0.1:8000`. FastAPI also provides SwaggerUI which can
be used interactively by pointing a browser to `http://127.0.0.1:8000/docs`.

### docker-build: Build a docker image

`make docker-build`

This requires that [Docker][11] is installed on your machine. Then this command
will build a docker image based on the given `Dockerfile` in the root folder of
the repository.

### run-container: Run the docker image

`make run-container`

Use this command if you have build your docker image via `make docker-build`.
Then a container will be started using these additional command line arguments:

  - `--rm`: Automatically remove the container when it exits
  - `-ti`: Allocate a pseudo-TTY and keep STDIN open even if not
           attached (then `CTRL`-`C` can be used to stop container)
  - `-p 8000:8000`: Publish container's port 8000 to the port 8000 of
                    the host machine
  - `--name "$IMAGE_NAME"`: Name the container for better monitoring
  - `"$IMAGE_TAG"`: Full qualified name of the docker image (`$IMAGE_NAME` + version information, e.g. "latest")

After that, you can access the backend the same way as mentioned before in the
run section (search for `make run`). The difference is that your requests will
point now to the dockerized app instead directly to your host system. The app
runs in the foreground and can be stopped by stopping the process, e.g. via
`CTRL+C`.

### run-compose: Start Fastapi app via `docker-compose`

`make run-compose`

If you want to start the whole network with all attached services encapsulated
in Docker files, then you can run the provided `docker-compose.yml` file,
located in the root directory, via `docker-compose` command. It requires that
[Docker Compose][12] is installed. To see which versions of Docker Engine and
Docker Compose should be installed on your system, look at the version number
in the `docker-compose.yml` (e.g. `version: "3.5"`) file and compare it with
the [compatibility matrix in the Docker Compose documentation][13].

The command will start the app in the background. So please note, that you have
to stop the services manually afterwards. If you do not shut down the started
services, they will eventually be restarted for you again, even after a system
reboot. You can use the provided command `make stop-compose` for that.

### stop-compose: Shut down all docker-compose components

`make stop-compose`

Shut down all services and networks configured in `docker-compose.yml`. This
is necessary to avoid unwanted restarts of services, even after the host
machine was restarted. This is only necessary if the Docker Compose file was
started via `docker-compose -f docker-compose.yml` or via `make run-compose`,
of course. 

## Debug the app

For running the app in debug mode, you can best integrate it in an IDE and
simply run `application.py` in debug mode. It requires that the libraries are
installed, i.e. `poetry` is working correctly. You can find out 
[more about debugging FastAPI in the tutorial][10].

## Learn more

- [Python][1] is one of the most loved and wanted programming languages since
  years (see https://insights.stackoverflow.com/survey). Python tries to be as
  simple as possible for programmers. You can write really beautiful code with
  Python.
- [FastAPI][2] has an excellent documentation and tries to keep things simple.
  It will also be a pleasure for you to work with FastAPI. It is a modern, fast
  (high-performance), web framework for building APIs with Python 3.6+ based on
  standard Python type hints. It is also possible to use FastAPI as a kind of
  interface, so that dependencies and risks are minimised (dependency
  injection).


[1]: https://python.org
[2]: https://fastapi.tiangolo.com
[3]: https://python-poetry.org/
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
