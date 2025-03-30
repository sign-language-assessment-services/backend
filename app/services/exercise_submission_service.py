from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.exercise_submission import ExerciseSubmission
from app.repositories.exercise_submissions import (
    add_exercise_submission, get_exercise_submission, list_exercise_submissions
)
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
