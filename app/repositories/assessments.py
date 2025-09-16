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
    assessment_without_tasks = assessment.model_dump(exclude={"tasks"})
    db_model = assessment_to_db(Assessment(**assessment_without_tasks))

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
        session.add_all(tasks_links)
        session.flush()

    add_entry(session, db_model)

def get_assessment(session: Session, _id: UUID) -> Assessment | None:
    result = get_by_id(session, DbAssessment, _id)
    if result:
        return assessment_to_domain(result)
    return None


def list_assessments(session: Session) -> list[Assessment]:
    logger.info("Requesting all assessments from database.")
    results = get_all(session, DbAssessment)
    return [assessment_to_domain(result) for result in results]


def update_assessment(session: Session, _id: UUID, **kwargs: Any) -> None:
    update_entry(session, DbAssessment, _id, **kwargs)


def delete_assessment(session: Session, _id: UUID) -> None:
    delete_entry(session, DbAssessment, _id)
