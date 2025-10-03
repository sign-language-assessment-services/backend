import logging
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.assessment_submission import AssessmentSubmission
from app.database.tables.assessment_submissions import DbAssessmentSubmission
from app.mappers.assessment_submission_mapper import (
    assessment_submission_to_db, assessment_submission_to_domain
)
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry

logger = logging.getLogger(__name__)


def add_assessment_submission(session: Session, submission: AssessmentSubmission) -> None:
    db_model = assessment_submission_to_db(submission)
    logger.info(
        "Requesting add assessment submission %(_id)s with session id %(session_id)s.",
        {"_id": db_model.id, "session_id": id(session)}
    )
    add_entry(session, db_model)


def get_assessment_submission(session: Session, _id: UUID) -> AssessmentSubmission | None:
    logger.info(
        "Requesting assessment submission %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    result = get_by_id(session, DbAssessmentSubmission, _id)
    if result:
        return assessment_submission_to_domain(result)
    return None


def list_assessment_submissions(session: Session) -> list[AssessmentSubmission]:
    logger.info(
        "Requesting all assessment submissions with session id %(session_id)s.",
        {"session_id": id(session)}
    )
    result = get_all(session, DbAssessmentSubmission)
    return [assessment_submission_to_domain(r) for r in result]


def update_assessment_submission(session: Session, _id: UUID, **kwargs: Any) -> None:
    logger.info(
        "Requesting update assessment submission %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    update_entry(session, DbAssessmentSubmission, _id, **kwargs)


def delete_assessment_submission(session: Session, _id: UUID) -> None:
    logger.info(
        "Requesting delete assessment submission %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    delete_entry(session, DbAssessmentSubmission, _id)
