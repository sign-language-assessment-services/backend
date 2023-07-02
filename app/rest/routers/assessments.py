# pylint: disable=unused-argument

from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends

from app.authorization.auth_bearer import JWTBearer
from app.core.models.assessment import Assessment
from app.services.assessment_service import AssessmentService

router = APIRouter(dependencies=[Depends(JWTBearer())])

# TODO: Rollen/User decorator wieder möglich machen
# TODO: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
# TODO: Allgemeines Code-Refactoring


@router.get("/assessments/{assessment_id}")
# @requires("slas-frontend-user")
async def read_assessment(
        assessment_id: int,
        assessment_service: Annotated[AssessmentService, Depends()],
) -> Assessment:
    return assessment_service.get_assessment_by_id(assessment_id)


@router.post("/assessments/{assessment_id}/submissions/")
# @requires("test-taker")
async def process_submission(
        assessment_id: int,
        submission: Dict[int, List[int]],
        assessment_service: Annotated[AssessmentService, Depends()]
) -> dict[str, int]:
    return assessment_service.score_assessment(assessment_id, submission)
