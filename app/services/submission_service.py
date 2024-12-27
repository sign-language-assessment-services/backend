from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.submission import Submission
from app.repositories.submissions import (
    add_submission, get_submission, list_assessment_submissions_for_user, list_submissions
)
from app.settings import get_settings


class SubmissionService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def add_submission(session: Session, submission: Submission) -> None:
        add_submission(session=session, submission=submission)

    @staticmethod
    def get_submission(session: Session, submission_id: UUID) -> Submission:
        return get_submission(session=session, _id=submission_id)

    @staticmethod
    def list_submissions(session: Session) -> list[Submission]:
        return list_submissions(session=session)

    @staticmethod
    def get_all_submissions_for_assessment_and_user(
            session: Session,
            user_name: UUID,
            assessment_id: UUID
    ) -> list[Submission]:
        return list_assessment_submissions_for_user(
            session=session,
            user_name=user_name,
            assessment_id=assessment_id
        )
