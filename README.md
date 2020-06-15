# Sign Language Assessment Services - Backend

This app is written in [Python][1] version 3.7 and uses the [FastAPI][2] framework.

## Prerequisites

The following software is required to use this app:

- [Python3.7][1]
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

### Build

`./go build`

Install all libraries used by the app via pipenv. To understand what pipenv is doing under the hood,
please refer to the [pipenv documentation][3].

### Test

`./go test`

Launches all unit test files in `./test` folder via [pytest][8] which will be installed in the build step using `./go build`.

### Lint

`./go lint`

Checks if all python files are written according to coding guidelines. This is done by using [pylint][9].

### Run

`./go run`

Runs the app in development mode, i.e. starting a uvicorn server which allows requests to `http://localhost:8000`.
FastAPI also provides SwaggerUI which can be used interactively by pointing a browser to `http://127.0.0.1:8000/docs`.

### Build, test, lint and run

`./go all`

Do every task defined in the build automation script, i.e. build the application, test and lint the code, and if no error occured,
finally run the app.


## Learn more

- [Python][1] is one of the most loved and wanted programming languages (see https://insights.stackoverflow.com/survey/2019).
  Python tries to be as simple as possible for programmers. You can really write wonderful, beautiful code with Python.
- [FastAPI][2] has an excellent documentation and tries to keep things simple. It will also be a pleasure for you to work with FastAPI.


[1]: https://python.org
[2]: https://fastapi.tiangolo.com
[3]: https://github.com/pypa/pipenv
[4]: https://www.gnu.org/software/bash
[5]: https://gitforwindows.org
[6]: https://docs.microsoft.com/windows/wsl/install-win10
[7]: https://www.cygwin.com
[8]: https://docs.pytest.org
[9]: https://www.pylint.org
