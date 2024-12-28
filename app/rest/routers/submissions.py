from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.core.models.submission import Submission
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.rest.routers.assessments import router
from app.services.exercise_service import ExerciseService
from app.services.submission_service import SubmissionService


@router.get("/submissions/{submission_id}")
async def get_submission(
        submission_id: UUID,
        submission_service: Annotated[SubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> Submission:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    return submission_service.get_submission(session=db_session, submission_id=submission_id)


@router.get("/submissions/")
async def list_submissions(
        submission_service: Annotated[SubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> list[Submission]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    return submission_service.list_submissions(session=db_session)


@router.get("/assessments/{assessment_id}/exercises/{exercise_id}/submissions/")
async def list_assessment_exercise_submissions_for_user(
        assessment_id: UUID,
        exercise_id: UUID,
        submission_service: Annotated[SubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session),
) -> list[Submission]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    submissions = submission_service.get_all_submissions_for_assessment_and_user(
        session=db_session,
        user_name=UUID(current_user.id),
        assessment_id=assessment_id
    )
    return [s for s in submissions if s.exercise_id == exercise_id]


@router.post("/assessments/{assessment_id}/exercises/{exercise_id}/submissions/")
async def post_submission(
        assessment_id: UUID,
        exercise_id: UUID,
        answers: MultipleChoiceAnswer,
        submission_service: Annotated[SubmissionService, Depends()],
        exercise_service: Annotated[ExerciseService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session),
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    multiple_choice_id = exercise_service.get_exercise_by_id(
        session=db_session, exercise_id=exercise_id
    ).question_type.content.id

    submission = Submission(
        user_name=current_user.id,
        assessment_id=assessment_id,
        exercise_id=exercise_id,
        multiple_choice_id=multiple_choice_id,
        answer=answers
    )
    submission_service.add_submission(session=db_session, submission=submission)
    return submission
