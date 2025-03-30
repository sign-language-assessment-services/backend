from app.core.models.assessment_submission import AssessmentSubmission
from app.database.tables.assessment_submissions import DbAssessmentSubmission


def assessment_submission_to_domain(db_submission: DbAssessmentSubmission) -> AssessmentSubmission:
    return AssessmentSubmission(
        id=db_submission.id,
        created_at=db_submission.created_at,
        user_id=db_submission.user_id,
        score=db_submission.score,
        finished_at=db_submission.finished_at,
        assessment_id=db_submission.assessment_id
    )


def assessment_submission_to_db(submission: AssessmentSubmission) -> DbAssessmentSubmission:
    return DbAssessmentSubmission(
        id=submission.id,
        created_at=submission.created_at,
        user_id=submission.user_id,
        score=submission.score,
        finished_at=submission.finished_at,
        assessment_id=submission.assessment_id
    )
