from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.score import Score
from app.core.models.submission import Submission
from app.repositories.assessments import get_assessment_by_id, list_assessments
from app.repositories.submissions import add_submission, list_submissions_for_user
from app.services.object_storage_client import ObjectStorageClient
from app.settings import get_settings
from app.type_hints import AssessmentAnswers


class AssessmentService:
    def __init__(
            self,
            object_storage_client: Annotated[ObjectStorageClient, Depends()],
            settings: Annotated[Settings, Depends(get_settings)],
    ):
        self.object_storage_client = object_storage_client
        self.settings = settings

    @staticmethod
    def get_assessment_by_id(session: Session, assessment_id: UUID) -> Assessment | None:
        return get_assessment_by_id(session=session, _id=assessment_id)


    @staticmethod
    def list_assessments(session: Session) -> list[Assessment]:
        return list_assessments(session=session)


    def score_assessment(
            self,
            assessment_id: UUID,
            answers: AssessmentAnswers,
            user_id: str,
            session: Session
    ) -> Score:
        assessment = self.get_assessment_by_id(session=session, assessment_id=assessment_id)
        score = assessment.score(answers=answers)
        submission = Submission(
            user_name=user_id,
            assessment_id=assessment_id,
            answers=answers,
            points=score.points,
            maximum_points=score.maximum_points,
            percentage=score.percentage
        )
        add_submission(session=session, submission=submission)  # submission=DbExerciseSubmission.from_submission(submission))
        return score

    @staticmethod
    def list_submissions(session: Session, user_id) -> list[Submission]:
        return list_submissions_for_user(session=session, user_id=user_id)
