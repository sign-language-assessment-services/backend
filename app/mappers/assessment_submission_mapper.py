import logging

from app.core.models.assessment_submission import AssessmentSubmission
from app.database.tables.assessment_submissions import DbAssessmentSubmission

logger = logging.getLogger(__name__)


def assessment_submission_to_domain(db_submission: DbAssessmentSubmission) -> AssessmentSubmission:
    logger.info("Transform DbAssessmentSubmission into domain model object.")
    assessment_submission = AssessmentSubmission(
        id=db_submission.id,
        created_at=db_submission.created_at,
        user_id=db_submission.user_id,
        score=db_submission.score,
        finished=db_submission.finished,
        finished_at=db_submission.finished_at,
        assessment_id=db_submission.assessment_id
    )
    return assessment_submission


def assessment_submission_to_db(submission: AssessmentSubmission) -> DbAssessmentSubmission:
    logger.info("Transform assessment submission into database object.")
    db_assessment_submission = DbAssessmentSubmission(
        id=submission.id,
        created_at=submission.created_at,
        user_id=submission.user_id,
        score=submission.score,
        finished=submission.finished,
        finished_at=submission.finished_at,
        assessment_id=submission.assessment_id
    )
    logger.info(
        "Assessment submission database object with id %(_id)s created.",
        {"_id": db_assessment_submission.id}
    )
    return db_assessment_submission
