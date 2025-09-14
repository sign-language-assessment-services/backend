from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.assessment_submission import AssessmentSubmission
from app.database.tables.assessment_submissions import DbAssessmentSubmission
from app.mappers.assessment_submission_mapper import (
    assessment_submission_to_db, assessment_submission_to_domain
)
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry


def add_assessment_submission(session: Session, submission: AssessmentSubmission) -> None:
    db_model = assessment_submission_to_db(submission)
    add_entry(session, db_model)


def get_assessment_submission(session: Session, _id: UUID) -> AssessmentSubmission | None:
    result = get_by_id(session, DbAssessmentSubmission, _id)
    if result:
        return assessment_submission_to_domain(result)
    return None


def list_assessment_submissions(session: Session) -> list[AssessmentSubmission]:
    result = get_all(session, DbAssessmentSubmission)
    return [assessment_submission_to_domain(r) for r in result]


def update_assessment_submission(session: Session, _id: UUID, **kwargs: Any) -> None:
    update_entry(session, DbAssessmentSubmission, _id, **kwargs)


def delete_assessment_submission(session: Session, _id: UUID) -> None:
    delete_entry(session, DbAssessmentSubmission, _id)
