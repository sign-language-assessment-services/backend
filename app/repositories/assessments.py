import logging
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.database.tables.assessments import DbAssessment
from app.database.tables.assessments_tasks import DbAssessmentsTasks
from app.mappers.assessment_mapper import assessment_to_db, assessment_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry

logger = logging.getLogger(__name__)


def add_assessment(session: Session, assessment: Assessment) -> None:
    # TODO: see if it can be simplified like in multiple choice
    assessment_without_tasks = assessment.model_dump(exclude={"tasks"})
    db_model = assessment_to_db(Assessment(**assessment_without_tasks))
    logger.debug(
        "Requesting add assessment %(_id)s with session id %(session_id)s.",
        {"_id": db_model.id, "session_id": id(session)}
    )
    session.add(db_model)
    session.flush()

    if assessment.tasks:
        tasks_links = [
            DbAssessmentsTasks(
                assessment_id=db_model.id,
                task_id=task.id,
                position=i
            )
            for i, task in enumerate(assessment.tasks, start=1)
        ]
        logger.debug(
            "Requesting adding %(n)d tasks for assessment %(_id)s with session id %(session_id)s.",
            {"n": len(tasks_links), "_id": db_model.id, "session_id": id(session)}
        )
        session.add_all(tasks_links)
        session.flush()

    logger.debug(
        "Requesting add full assessment %(_id)s with session id %(session_id)s.",
        {"_id": db_model.id, "session_id": id(session)}
    )
    add_entry(session, db_model)

def get_assessment(session: Session, _id: UUID) -> Assessment | None:
    logger.debug(
        "Requesting assessment %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    result = get_by_id(session, DbAssessment, _id)
    if result:
        return assessment_to_domain(result)
    return None


def list_assessments(session: Session) -> list[Assessment]:
    logger.debug(
        "Requesting all assessments with session id %(session_id)s.",
        {"session_id": id(session)}
    )
    results = get_all(session, DbAssessment)
    return [assessment_to_domain(result) for result in results]


def update_assessment(session: Session, _id: UUID, **kwargs: Any) -> None:
    logger.debug(
        "Requesting update assessment %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    update_entry(session, DbAssessment, _id, **kwargs)


def delete_assessment(session: Session, _id: UUID) -> None:
    logger.debug(
        "Requesting delete assessment %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    delete_entry(session, DbAssessment, _id)
