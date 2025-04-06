from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.authorization.auth_bearer import JWTBearer
from app.core.models.exercise_submission import ExerciseSubmission
from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.rest.responses.exercise_submissions import (
    ExerciseSubmissionListResponse, ExerciseSubmissionResponse
)
from app.services.exercise_service import ExerciseService
from app.services.exercise_submission_service import ExerciseSubmissionService
from app.services.scoring_service import ScoringService

router = APIRouter(dependencies=[Depends(JWTBearer())])


@router.get("/exercise_submissions/{submission_id}", response_model=ExerciseSubmissionResponse)
async def get_submission(
        submission_id: UUID,
        submission_service: Annotated[ExerciseSubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> ExerciseSubmission:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    submission = submission_service.get_submission_by_id(db_session, submission_id)
    if not submission:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return submission


@router.get("/exercise_submissions/", response_model=list[ExerciseSubmissionListResponse])
async def list_submissions(
        submission_service: Annotated[ExerciseSubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> list[ExerciseSubmission]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return submission_service.list_submissions(session=db_session)


@router.post(
    "/assessment_submissions/{assessment_submission_id}/exercises/{exercise_id}/submissions/",
    response_model=ExerciseSubmissionResponse
)
async def post_submission(
        assessment_submission_id: UUID,
        exercise_id: UUID,
        answers: MultipleChoiceAnswer,
        submission_service: Annotated[ExerciseSubmissionService, Depends()],
        exercise_service: Annotated[ExerciseService, Depends()],
        scoring_service: Annotated[ScoringService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session),
) -> ExerciseSubmission:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    submission = ExerciseSubmission(
        user_id=current_user.id if current_user.id else uuid4(),  # TODO: temporary activate uuid for user
        answer=answers,
        assessment_submission_id=assessment_submission_id,
        exercise_id=exercise_id,
    )
    exercise = exercise_service.get_exercise_by_id(db_session, exercise_id)
    scoring_service.score(exercise_submission=submission, exercise=exercise)
    submission_service.add_submission(session=db_session, submission=submission)
    return submission
