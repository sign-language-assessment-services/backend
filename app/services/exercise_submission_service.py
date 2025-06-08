from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.exercise_submission import ExerciseSubmission
from app.repositories.exercise_submissions import (
    add_exercise_submission, get_exercise_submission, list_exercise_submissions,
    upsert_exercise_submission
)
from app.services.exceptions import ExerciseSubmissionNotExistsException
from app.settings import get_settings


class ExerciseSubmissionService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def add_submission(session: Session, submission: ExerciseSubmission) -> None:
        add_exercise_submission(session=session, submission=submission)

    @staticmethod
    def get_submission_by_id(session: Session, submission_id: UUID) -> ExerciseSubmission | None:
        return get_exercise_submission(session=session, _id=submission_id)

    @staticmethod
    def list_submissions(session: Session) -> list[ExerciseSubmission]:
        return list_exercise_submissions(session=session)

    def update_submission(self, session: Session, submission_id: UUID, **kwargs: str) -> ExerciseSubmission:
        exercise_submission = self.get_submission_by_id(session, submission_id)
        if not exercise_submission:
            raise ExerciseSubmissionNotExistsException(
                f"No exercise submission found with id {submission_id}."
            )
        for key, value in kwargs.items():
            setattr(exercise_submission, key, value)
        session.commit()
        return exercise_submission

    @staticmethod
    def upsert_submission(session: Session, submission: ExerciseSubmission) -> None:
        upsert_exercise_submission(session=session, submission=submission)
