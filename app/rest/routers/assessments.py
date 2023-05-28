# pylint: disable=unused-argument

from typing import Dict, List, Annotated

from fastapi import APIRouter, Depends
from starlette.authentication import requires
from starlette.requests import Request

from app.core.models.assessment import Assessment
from app.services.assessment_service import AssessmentService

router = APIRouter()


@router.get("/assessments/{assessment_id}")
# @requires("slas-frontend-user")
async def read_assessment(
        assessment_id: int,
        request: Request,
        assessment_service: Annotated[AssessmentService, Depends()]
) -> Assessment:
    return assessment_service.get_assessment_by_id(assessment_id)


@router.post("/assessments/{assessment_id}/submissions/")
# @requires("test-taker")
async def process_submission(
        assessment_id: int,
        submission: Dict[int, List[int]],
        request: Request,
        assessment_service: Annotated[AssessmentService, Depends()]
) -> dict[str, int]:
    return assessment_service.score_assessment(assessment_id, submission)
