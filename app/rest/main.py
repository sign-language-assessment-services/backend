import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.database.orm import import_tables, run_migrations
from app.docs.openapi_description import DESCRIPTION
from app.docs.openapi_summary import SUMMARY
from app.log.config.setup_logging import setup_logging
from app.rest.routers import (
    assessment_submissions, assessments, choices, exercise_submissions, exercises, multimedia_files,
    multiple_choices, primers, root
)

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Logger is successfully configured.")


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Running migrations.")
    run_migrations()
    logger.info("Finished running migrations.")
    yield
    logger.info("Closing lifespan context.")


def create_app() -> FastAPI:
    logger.info("Creating FastAPI app.")
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
        lifespan=lifespan
    )
    logger.info("Importing tables.")
    import_tables()

    logger.info("Adding routers.")
    app.include_router(root.router)
    app.include_router(assessments.router)
    app.include_router(primers.router)
    app.include_router(exercises.router)
    app.include_router(multiple_choices.router)
    app.include_router(choices.router)
    app.include_router(multimedia_files.router)
    app.include_router(assessment_submissions.router)
    app.include_router(exercise_submissions.router)
    logger.info("Finished adding routers.")
    return app
