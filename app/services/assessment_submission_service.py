from datetime import datetime, timezone
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.assessment_submission import AssessmentSubmission
from app.repositories.assessment_submissions import (
    add_assessment_submission, get_assessment_submission, list_assessment_submissions,
    update_assessment_submission
)
from app.repositories.exercise_submissions import get_exercise_submissions_for_assessment_submission
from app.settings import get_settings


class AssessmentSubmissionService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def add_submission(session: Session, submission: AssessmentSubmission) -> None:
        add_assessment_submission(session=session, submission=submission)

    @staticmethod
    def get_submission_by_id(session: Session, submission_id: UUID) -> AssessmentSubmission:
        return get_assessment_submission(session=session, _id=submission_id)

    @staticmethod
    def list_submissions(session: Session) -> list[AssessmentSubmission]:
        return list_assessment_submissions(session=session)

    @staticmethod
    def update_submission(session: Session, submission_id: UUID, **kwargs: Any) -> AssessmentSubmission:
        if kwargs.get("finished"):
            exercise_submissions = get_exercise_submissions_for_assessment_submission(
                session=session,
                assessment_submission_id=submission_id
            )
            total_score = sum(
                exercise_submission.score or 0
                for exercise_submission in exercise_submissions
            )
            kwargs["score"] = total_score
            kwargs["finished_at"] = datetime.now(timezone.utc)

        update_assessment_submission(session, submission_id, **kwargs)
        return get_assessment_submission(session, submission_id)
