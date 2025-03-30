from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.assessment_submission import AssessmentSubmission
from app.repositories.assessment_submissions import (
    add_submission, get_submission, list_submissions
)
from app.settings import get_settings


class AssessmentSubmissionService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def add_submission(session: Session, submission: AssessmentSubmission) -> None:
        add_submission(session=session, submission=submission)

    @staticmethod
    def get_submission_by_id(session: Session, submission_id: UUID) -> AssessmentSubmission:
        return get_submission(session=session, _id=submission_id)

    @staticmethod
    def list_submissions(session: Session) -> list[AssessmentSubmission]:
        return list_submissions(session=session)
