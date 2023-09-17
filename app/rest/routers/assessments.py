# pylint: disable=unused-argument

from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.authorization.auth_bearer import JWTBearer
from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.submission import Submission
from app.core.models.user import User
from app.database.orm import get_db_session
from app.services.assessment_service import AssessmentService

router = APIRouter(dependencies=[Depends(JWTBearer())])


async def get_current_user(user: Annotated[User, Depends(JWTBearer())]) -> User:
    return user


@router.get("/assessments/{assessment_id}")
async def read_assessment(
        assessment_id: str,
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)]
) -> Assessment:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return assessment_service.get_assessment_by_id(assessment_id)


@router.get("/assessments/")
async def list_assessments(
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)]
) -> list[AssessmentSummary]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return assessment_service.list_assessments()


@router.get("/submissions/")
async def list_submissions(
        user_id: str,
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> list[Submission]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    if current_user.id != user_id and "test-scorer" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return assessment_service.list_submissions(user_id=user_id, session=db_session)


@router.post("/assessments/{assessment_id}/submissions/")
async def process_submission(
        assessment_id: str,
        answers: Dict[int, List[int]],
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> dict[str, int|float]:
    if "test-taker" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return assessment_service.score_assessment(assessment_id, answers, current_user.id, db_session)
