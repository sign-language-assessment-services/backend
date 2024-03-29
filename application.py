"""Get Fastapi app object and run it only if directly invoked

This file provides the app object from `app.main` directly. It can be
used to start a (u)wsgi server which handles the app object or using
gunicorn or similar webserver.

The file can also be started as a script. Then `uvicorn` will start the
app being a local web server. This is very helpful to debug the app as
described here: https://fastapi.tiangolo.com/tutorial/debugging/ .
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
