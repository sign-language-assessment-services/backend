from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.database.tables.assessments import DbAssessment
from app.database.tables.assessments_tasks import DbAssessmentsTasks
from app.mappers.assessment_mapper import assessment_to_db, assessment_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry


def add_assessment(session: Session, assessment: Assessment) -> None:
    db_model = assessment_to_db(assessment)
    if db_model.tasks:
        session.add(db_model)
        session.add_all(db_model.tasks)
        session.flush()

        db_model.tasks_link = [
            DbAssessmentsTasks(position=i, task=task)
            for i, task in enumerate(db_model.tasks, start=1)
        ]
        session.commit()
        return None

    add_entry(session, db_model)
    return None


def get_assessment(session: Session, _id: UUID) -> Assessment | None:
    result = get_by_id(session, DbAssessment, _id)
    if result:
        return assessment_to_domain(result)
    return None


def list_assessments(session: Session) -> list[Assessment]:
    results = get_all(session, DbAssessment)
    return [assessment_to_domain(result) for result in results]


def update_assessment(session: Session, _id: UUID, **kwargs: Any) -> None:
    update_entry(session, DbAssessment, _id, **kwargs)


def delete_assessment(session: Session, _id: UUID) -> None:
    delete_entry(session, DbAssessment, _id)
