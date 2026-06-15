import logging

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.database.orm import import_tables
from app.docs.openapi_description import DESCRIPTION
from app.docs.openapi_summary import SUMMARY
from app.log.config.setup_logging import setup_logging
from app.rest.routers import (
    assessment_submissions, assessments, choices, exercise_submissions, exercises, multimedia_files,
    multiple_choices, primers, root, users
)
from app.services.exceptions.external_service import ExternalServiceException
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
        default_response_class=JSONResponse
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
    app.include_router(users.router)

    logger.info("Register global exception handlers.")
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(ExternalServiceException, external_service_exception_handler)

    logger.info("FastAPI app successfully created.")
    return app


async def not_found_exception_handler(_, exc: NotFoundException) -> JSONResponse:
    detail = str(exc) if str(exc) else "Resource not found."

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": detail},
    )


async def external_service_exception_handler(_, exc: ExternalServiceException) -> JSONResponse:
    detail = str(exc) if str(exc) else "External service error."

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": detail},
    )
