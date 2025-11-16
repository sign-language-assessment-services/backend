from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.assessment_submission import AssessmentSubmission
from app.repositories.assessment_submissions import (
    add_assessment_submission, get_assessment_submission, list_assessment_submissions,
    update_assessment_submission
)
from app.repositories.exercise_submissions import get_exercise_submissions_for_assessment_submission
from app.rest.filters.assessment_submissions import AssessmentSubmissionPick
from app.services.exceptions.not_found import AssessmentSubmissionNotFoundException


class AssessmentSubmissionService:
    @staticmethod
    def create_assessment_submission(session: Session, user_id: UUID, assessment_id: UUID) -> AssessmentSubmission:
        submission = AssessmentSubmission(user_id=user_id, assessment_id=assessment_id)
        add_assessment_submission(session=session, submission=submission)
        return submission

    @staticmethod
    def get_assessment_submission_by_id(session: Session, submission_id: UUID) -> AssessmentSubmission:
        if result := get_assessment_submission(session=session, _id=submission_id):
            return result
        raise AssessmentSubmissionNotFoundException(f"Assessment submission with id '{submission_id}' not found.")

    @staticmethod
    def list_assessment_submissions(
            session: Session,
            user_id: UUID | None = None,
            pick_strategy: AssessmentSubmissionPick | None = None
    ) -> list[AssessmentSubmission]:
        return list_assessment_submissions(
            session=session,
            user_id=user_id,
            pick_strategy=pick_strategy
        )

    @staticmethod
    def update_assessment_submission(session: Session, submission_id: UUID, **kwargs: Any) -> AssessmentSubmission:
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
