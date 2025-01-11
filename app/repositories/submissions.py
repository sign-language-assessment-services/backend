from typing import Any
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.core.models.submission import Submission
from app.database.tables.submissions import DbSubmission
from app.mappers.submission_mapper import submission_to_db, submission_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry


def add_submission(session: Session, submission: Submission) -> None:
    db_model = submission_to_db(submission)
    add_entry(session, db_model)


def get_submission(session: Session, _id: UUID) -> Submission | None:
    result = get_by_id(session, DbSubmission, _id)
    if result:
        return submission_to_domain(result)
    return None


def list_submissions(session: Session) -> list[Submission]:
    result = get_all(session, DbSubmission)
    return [submission_to_domain(r) for r in result]


def list_submissions_for_user(session: Session, user_id: UUID) -> list[Submission]:
    filter_conditions = {DbSubmission.user_id: user_id}
    result = get_all(session, DbSubmission, filter_by=filter_conditions)
    return [submission_to_domain(r) for r in result]


def list_assessment_submissions_for_user(session: Session, user_id: UUID, assessment_id: UUID) -> list[Submission]:
    filter_conditions = {
        DbSubmission.assessment_id: assessment_id,
        DbSubmission.user_id: user_id
    }
    result = get_all(session, DbSubmission, filter_by=filter_conditions)
    return [submission_to_domain(r) for r in result]


def list_latest_assessment_submissions_for_user(
        session: Session,
        user_id: UUID,
        assessment_id: UUID
) -> list[Submission]:
    subquery = (
        select(
            DbSubmission.exercise_id,
            func.max(DbSubmission.created_at).label("max_created_at")
        )
        .where(
            and_(
                DbSubmission.assessment_id == assessment_id,
                DbSubmission.user_id == user_id
            )
        )
        .group_by(DbSubmission.exercise_id)
    ).subquery("latest_submissions")

    query = (
        select(DbSubmission)
        .join(
            subquery,
            and_(
                DbSubmission.exercise_id == subquery.c.exercise_id,
                DbSubmission.created_at == subquery.c.max_created_at
            )
        )
    )
    result = session.execute(query).unique().scalars().all()
    return [submission_to_domain(r) for r in result]


def update_submission(session: Session, _id: UUID, **kwargs: Any) -> None:
    update_entry(session, DbSubmission, _id, **kwargs)


def delete_submission(session: Session, _id: UUID) -> None:
    delete_entry(session, DbSubmission, _id)
