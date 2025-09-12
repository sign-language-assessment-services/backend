from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.exercise_submission import ExerciseSubmission
from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.repositories.exercise_submissions import (
    add_exercise_submission, get_exercise_submission, list_exercise_submissions,
    upsert_exercise_submission
)
from app.services.exercise_service import ExerciseService
from app.services.scoring_service import ScoringService
from app.settings import get_settings


class ExerciseSubmissionService:
    def __init__(
            self,
            settings: Annotated[Settings, Depends(get_settings)],
            scoring_service: Annotated[ScoringService, Depends()],
            exercise_service: Annotated[ExerciseService, Depends()]
    ):
        self.settings = settings
        self.exercise_service = exercise_service
        self.scoring_service = scoring_service

    def create_exercise_submission(
            self,
            session: Session,
            assessment_submission_id: UUID,
            exercise_id: UUID,
            answer_ids: list[UUID]
    ) -> None:
        multiple_choice_answer = MultipleChoiceAnswer(
            choices=answer_ids
        )
        exercise_submission = ExerciseSubmission(
            assessment_submission_id=assessment_submission_id,
            exercise_id=exercise_id,
            answer=multiple_choice_answer,
            score=None
        )
        exercise = self.exercise_service.get_exercise_by_id(
            session=session,
            exercise_id=exercise_id
        )
        self.scoring_service.score(
            exercise_submission=exercise_submission,
            exercise=exercise
        )
        add_exercise_submission(
            session=session,
            submission=exercise_submission
        )

    @staticmethod
    def get_exercise_submission_by_id(session: Session, submission_id: UUID) -> ExerciseSubmission | None:
        return get_exercise_submission(session=session, _id=submission_id)

    @staticmethod
    def list_exercise_submissions(session: Session) -> list[ExerciseSubmission]:
        return list_exercise_submissions(session=session)

    def upsert_exercise_submission(
            self,
            session: Session,
            data: dict[str, Any],
            assessment_submission_id: UUID,
            exercise_id: UUID
    ) -> ExerciseSubmission:
        choices = data.pop("answer")
        exercise_submission = ExerciseSubmission(
            **data,
            answer=MultipleChoiceAnswer(choices=choices),
            assessment_submission_id=assessment_submission_id,
            exercise_id=exercise_id
        )
        exercise = self.exercise_service.get_exercise_by_id(
            session=session,
            exercise_id=exercise_id
        )
        self.scoring_service.score(
            exercise_submission=exercise_submission,
            exercise=exercise
        )
        upsert_exercise_submission(
            session=session,
            submission=exercise_submission
        )
        return exercise_submission
