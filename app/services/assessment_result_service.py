from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.assessment_result import AssessmentResult, ExerciseScore, SubmissionResult
from app.repositories.assessment_submissions import (
    list_finished_assessment_submissions_for_assessment
)


class AssessmentResultService:
    @staticmethod
    def get_assessment_result(session: Session, assessment_id: UUID) -> AssessmentResult:
        finished_assessment_submissions = list_finished_assessment_submissions_for_assessment(
            session=session,
            assessment_id=assessment_id,
        )
        submission_results = []
        for assessment_submission in finished_assessment_submissions:
            submission_results.append(
                SubmissionResult(
                    assessment_submission_id=assessment_submission.id,
                    user_id=assessment_submission.user_id,
                    exercise_scores=[
                        ExerciseScore(exercise_id=exercise_submission.id, score=exercise_submission.score)
                        for exercise_submission in assessment_submission.exercise_submissions
                    ],
                    total_score=assessment_submission.score,
                    finished_at=assessment_submission.finished_at
                )
            )
        return AssessmentResult(submissions=submission_results)
