from sqlalchemy.orm import Session

from app.core.models.submission import Submission
from app.database.tables.multiple_choice_submissions import DbMultipleChoiceSubmission
from app.mappers.submission_mapper import SubmissionMapper


def add_submission(session: Session, submission: Submission) -> None:
    db_model = SubmissionMapper.domain_to_db(submission)
    session.add(db_model)
    session.commit()
    return None


def get_submission_by_id(session: Session, _id: str) -> Submission | None:
    result = session.get(DbMultipleChoiceSubmission, {"id": _id})
    if result:
        model = SubmissionMapper.db_to_domain(result)
        return model
    return None


def list_submissions(session: Session) -> list[Submission]:
    results = session.query(DbMultipleChoiceSubmission).all()
    models = [SubmissionMapper.db_to_domain(result) for result in results]
    return models


def list_submissions_for_user(session: Session, user_id: str) -> list[Submission]:
    results = session.query(DbMultipleChoiceSubmission).filter_by(user_name=user_id).all()
    models = [SubmissionMapper.db_to_domain(result) for result in results]
    return models


def update_submission(session: Session, submission: Submission, **kwargs: dict[str, str]) -> None:
    session.query(DbMultipleChoiceSubmission).filter_by(id=submission.id).update(kwargs)
    session.commit()
    return None


def delete_submission_by_id(session: Session, _id: str) -> None:
    session.query(DbMultipleChoiceSubmission).filter_by(id=_id).delete()
    session.commit()
    return None
