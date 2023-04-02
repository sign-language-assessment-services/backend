import os

from fastapi import FastAPI
from fastapi_auth_middleware import AuthMiddleware

from app.authorization.verify_authorization_header import verify_authorization_header
from app.rest.routers import assessments, root


def create_app() -> FastAPI:
    verify_mandatory_env_variables()
    app = FastAPI()
    app.include_router(root.router)
    app.include_router(assessments.router)
    app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)
    return app


def verify_mandatory_env_variables() -> None:
    mandatory = (
        # Keycloak
        "ALGORITHMS", "API_AUDIENCE", "AUTH_ENABLED", "ISSUER", "JWKS_URL",
        # Minio
        "MINIO_BUCKET_NAME", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY"
    )
    for v in mandatory:
        if not os.getenv(v):
            raise EnvironmentError(f"Mandatory env variable {v} is not set.")
