import logging

from fastapi import FastAPI, status
from fastapi.responses import ORJSONResponse

from app.database.orm import import_tables
from app.docs.openapi_description import DESCRIPTION
from app.docs.openapi_summary import SUMMARY
from app.log.config.setup_logging import setup_logging
from app.rest.routers import (
    assessment_submissions, assessments, choices, exercise_submissions, exercises, multimedia_files,
    multiple_choices, primers, root
)
from app.services.exceptions.not_found import NotFoundException

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Logger is successfully configured.")


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
        default_response_class=ORJSONResponse
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

    logger.info("Register global exception handler.")
    app.add_exception_handler(NotFoundException, not_found_exception_handler)

    logger.info("FastAPI app successfully created.")
    return app


async def not_found_exception_handler(_, exc: NotFoundException):
    detail = str(exc) if str(exc) else "Resource not found."

    return ORJSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": detail},
    )
