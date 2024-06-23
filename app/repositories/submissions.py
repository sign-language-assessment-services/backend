from sqlalchemy.orm import Session

from app.core.models.submission import Submission
from app.database.tables.submissions import DbSubmission


def add_submission(session: Session, submission: Submission) -> None:
    session.add(DbSubmission.from_submission(submission))
    session.commit()


def list_submissions(session: Session) -> list[Submission]:
    result = session.query(DbSubmission).all()
    return [submission.to_submission() for submission in result]


def get_submission_by_id(session: Session, _id: str) -> Submission:
    result = session.query(DbSubmission).get({"id": _id})
    return result.to_submission()


def delete_submission_by_id(session: Session, _id: str) -> None:
    session.query(DbSubmission).filter_by(id=_id).delete()
    session.commit()


def list_submission_by_user_id(session: Session, user_id: str | None) -> list[DbSubmission]:
    if user_id:
        pass  # TODO: to be implemented
    result: list[DbSubmission] = session.query(DbSubmission).all()
    return [r.to_submission() for r in result]
