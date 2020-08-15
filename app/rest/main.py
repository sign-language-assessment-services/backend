from fastapi import FastAPI

from .routers import assessments, root


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(root.router)
    app.include_router(assessments.router)
    return app
