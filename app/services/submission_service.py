from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.score import Score
from app.core.models.submission import Submission
from app.repositories.submissions import (
    add_submission, get_submission_by_id, list_submissions
)
from app.settings import get_settings
from app.type_hints import SubmissionAnswers


class SubmissionService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def get_submission_by_id(session: Session, submission_id: UUID) -> Submission:
        return get_submission_by_id(session=session, _id=str(submission_id))

    @staticmethod
    def list_submissions(session: Session) -> list[Submission]:
        return list_submissions(session)

    def score_submission(
            self,
            assessment_id: UUID,
            answers: SubmissionAnswers,
            user_id: str,
            session: Session
    ) -> Score:
        assessment = self.get_assessment_by_id(session=session, assessment_id=assessment_id)
        score = assessment.score(answers=answers)
        submission = Submission(
            user_id=user_id,
            assessment_id=assessment_id,
            answers=answers,
            points=score.points,
            maximum_points=score.maximum_points,
            percentage=score.percentage
        )
        add_submission(session=session, submission=submission)  # submission=DbExerciseSubmission.from_submission(submission))
        return score

