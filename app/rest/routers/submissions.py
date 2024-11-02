from dataclasses import asdict
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.models.submission import Submission
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.rest.routers.assessments import router
from app.services.assessment_service import AssessmentService
from app.services.submission_service import SubmissionService
from app.type_hints import AssessmentAnswers


@router.get("/submissions/{submission_id}")
async def get_submission(
        submission_id: UUID,
        submission_service: Annotated[SubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> Submission:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    return submission_service.get_submission_by_id(session=db_session, submission_id=submission_id)


@router.get("/submissions/")
async def list_submissions(
        # user_id: str,
        submission_service: Annotated[SubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> list[Submission]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    # if current_user.id != user_id and "test-scorer" not in current_user.roles:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN)

    return submission_service.list_submissions(session=db_session)


@router.post("/assessments/{assessment_id}/submissions/")
async def process_submission(
        assessment_id: UUID,
        answers: AssessmentAnswers,
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> dict[str, float | int]:
    if "test-taker" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    score = assessment_service.score_assessment(assessment_id, answers, current_user.id, db_session)
    return asdict(score)
