from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.authorization.auth_bearer import JWTBearer
from app.core.models.score import Score
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.rest.responses.scores import ScoreResponse
from app.services.exercise_service import ExerciseService
from app.services.submission_service import SubmissionService

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.get("/assessments/{assessment_id}/score", response_model=ScoreResponse)
async def get_current_user_score_for_assessment(
        assessment_id: UUID,
        submission_service: Annotated[SubmissionService, Depends()],
        exercise_service: Annotated[ExerciseService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> Score:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    submissions = submission_service.get_latest_submissions_for_assessment_and_user(
        session=db_session,
        user_id=current_user.id,
        assessment_id=assessment_id
    )

    points = 0
    for submission in submissions:
        exercise = exercise_service.get_exercise_by_id(db_session, submission.exercise_id)
        multiple_choice = exercise.question_type.content
        selected_answers = submission.answer.choices
        correct_answers = [choice.id for choice in multiple_choice.choices if choice.is_correct]

        if set(selected_answers) == set(correct_answers):
            points += exercise.points

    return Score(
        assessment_id=assessment_id,
        user_id=current_user.id,
        points=points
    )
