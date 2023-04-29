from fastapi import FastAPI
from fastapi_auth_middleware import AuthMiddleware

from app.authorization.verify_authorization_header import verify_authorization_header
from app.rest.routers import assessments, root


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(root.router)
    app.include_router(assessments.router)
    app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)
    return app
