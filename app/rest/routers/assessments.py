# pylint: disable=unused-argument

from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.authorization.auth_bearer import JWTBearer
from app.core.models.assessment import Assessment
from app.core.models.user import User
from app.services.assessment_service import AssessmentService

router = APIRouter(dependencies=[Depends(JWTBearer())])


async def get_current_user(user: Annotated[User, Depends(JWTBearer())]):
    return user


@router.get("/assessments/{assessment_id}")
async def read_assessment(
        assessment_id: int,
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)]
) -> Assessment:
    if not "slas-frontend-user" in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return assessment_service.get_assessment_by_id(assessment_id)


@router.post("/assessments/{assessment_id}/submissions/")
async def process_submission(
        assessment_id: int,
        submission: Dict[int, List[int]],
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)]
) -> dict[str, int]:
    if not "test-taker" in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return assessment_service.score_assessment(assessment_id, submission)
