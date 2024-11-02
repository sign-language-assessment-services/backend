from sqlalchemy.orm import Session

from app.core.models.submission import Submission
from app.database.tables.multiple_choice_submissions import DbMultipleChoiceSubmission
from app.database.tables.submissions import DbSubmission
from app.mappers.submission_mapper import SubmissionMapper


def add_submission(session: Session, submission: Submission) -> None:
    session.add(DbSubmission.from_submission(submission))
    session.commit()


def list_submissions(session: Session) -> list[Submission]:
    results = session.query(DbMultipleChoiceSubmission).all()
    return [SubmissionMapper.db_to_domain(result) for result in results]


def get_submission_by_id(session: Session, _id: str) -> Submission:
    result = session.get(DbMultipleChoiceSubmission, {"id": _id})
    return SubmissionMapper.db_to_domain(result)


def delete_submission_by_id(session: Session, _id: str) -> None:
    session.query(DbSubmission).filter_by(id=_id).delete()
    session.commit()


def list_submissions_by_user_id(session: Session, user_id: str | None) -> list[Submission]:
    if user_id:
        results = session.query(DbMultipleChoiceSubmission).filter_by(user_name=user_id).all()
        return [SubmissionMapper.db_to_domain(result) for result in results]
    return list_submissions(session=session)
