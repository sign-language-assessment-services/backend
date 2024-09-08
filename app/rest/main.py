from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.docs.openapi_description import DESCRIPTION
from app.docs.openapi_summary import SUMMARY
from app.rest.routers import assessments, root, submissions


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
        default_response_class=ORJSONResponse
    )
    app.include_router(root.router)
    app.include_router(assessments.router)
    app.include_router(submissions.router)
    return app
