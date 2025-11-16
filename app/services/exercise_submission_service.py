import logging
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.models.exercise_submission import ExerciseSubmission
from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.repositories.exercise_submissions import (
    add_exercise_submission, get_exercise_submission, list_exercise_submissions,
    upsert_exercise_submission
)
from app.services.exceptions.not_found import ExerciseSubmissionNotFoundException
from app.services.exercise_service import ExerciseService
from app.services.scoring_service import ScoringService

logger = logging.getLogger(__name__)


class ExerciseSubmissionService:
    def __init__(
            self,
            scoring_service: Annotated[ScoringService, Depends()],
            exercise_service: Annotated[ExerciseService, Depends()]
    ):
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
        logger.info("Receive exercise submission %(_id)s", {"_id": submission_id})
        logger.debug(
            "Trying to receive exercise submission %(_id)s with session id %(session_id)s.",
            {"_id": submission_id, "session_id": id(session)}
        )
        if result := get_exercise_submission(session=session, _id=submission_id):
            return result
        raise ExerciseSubmissionNotFoundException(f"Exercise submission with id '{submission_id}' not found.")

    @staticmethod
    def list_exercise_submissions(
            session: Session,
            assessment_submission_id: UUID | None = None,
            exercise_id: UUID | None = None
    ) -> list[ExerciseSubmission]:
        return list_exercise_submissions(
            session=session,
            assessment_submission_id=assessment_submission_id,
            exercise_id=exercise_id
        )

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
