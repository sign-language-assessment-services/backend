from sqlalchemy.orm import Session

from app.core.models.submission import Submission


def add(session: Session, submission: Submission) -> None:
    session.add(submission)
    session.commit()
    return None


def list_by_user_id(session: Session, user_id: str) -> list[Submission]:
    return session.query(Submission).filter_by(user_id=user_id).all()
