from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.authorization.auth_bearer import JWTBearer
from app.core.models.assessment_submission import AssessmentSubmission
from app.core.models.exercise_submission import ExerciseSubmission
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.rest.responses.assessment_submissions import AssessmentSubmissionListResponse, AssessmentSubmissionResponse
from app.services.assessment_submission_service import AssessmentSubmissionService

router = APIRouter(dependencies=[Depends(JWTBearer())])


@router.get("/assessment_submissions/{submission_id}", response_model=AssessmentSubmissionResponse)
async def get_assessment_submission(
        submission_id: UUID,
        submission_service: Annotated[AssessmentSubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> AssessmentSubmission:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    submission = submission_service.get_submission_by_id(db_session, submission_id)
    if not submission:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return submission


@router.get("/assessment_submissions/", response_model=list[AssessmentSubmissionListResponse])
async def list_submissions(
        assessment_submission_service: Annotated[AssessmentSubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> list[ExerciseSubmission]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    return assessment_submission_service.list_submissions(session=db_session)


@router.post("/assessments/{assessment_id}/submissions/", response_model=AssessmentSubmissionResponse)
async def create_assessment_submission(
        assessment_id: UUID,
        submission_service: Annotated[AssessmentSubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session),
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    submission = AssessmentSubmission(
        user_id=current_user.id,
        assessment_id=assessment_id
    )
    submission_service.add_submission(session=db_session, submission=submission)
    return submission
