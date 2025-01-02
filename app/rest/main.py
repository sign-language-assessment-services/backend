from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.database.orm import import_tables, run_migrations
from app.docs.openapi_description import DESCRIPTION
from app.docs.openapi_summary import SUMMARY
from app.rest.routers import assessments, exercises, root, submissions


@asynccontextmanager
async def lifespan(_: FastAPI):
    run_migrations()
    yield
    print("Shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sign Language Portal API",
        description=DESCRIPTION,
        summary=SUMMARY,
        terms_of_service="tba",
        license_info={
            "name": "GPLv3",
            "url": "https://www.gnu.org/licenses/gpl-3.0.en.html"
        },
        contact={
            "name": "Sign Language Assessment Services GmbH",
            "email": "tbd@not-yet-available.zzz"
        },
        default_response_class=ORJSONResponse,
        lifespan=lifespan  # TODO: exceptions are not printed to console if lifespan is activated
    )
    import_tables()  # TODO: can be deleted after lifespan is permanently activated

    app.include_router(root.router)
    app.include_router(assessments.router)
    app.include_router(exercises.router)
    app.include_router(submissions.router)
    return app
