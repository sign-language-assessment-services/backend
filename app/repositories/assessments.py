from typing import Any
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.database.tables.assessments import DbAssessment
from app.mappers.assessment_mapper import AssessmentMapper


def add_assessment(session: Session, assessment: Assessment) -> None:
    db_model = AssessmentMapper.domain_to_db(assessment)
    session.add(db_model)
    session.commit()


def get_assessment_by_id(session: Session, _id: UUID) -> Assessment | None:
    result = session.execute(select(DbAssessment).filter_by(id=_id)).scalar_one_or_none()
    if result:
        model = AssessmentMapper.db_to_domain(result)
        return model


def list_assessments(session: Session) -> list[Assessment]:
    results = session.execute(select(DbAssessment)).scalars().all()
    models = [AssessmentMapper.db_to_domain(result) for result in results]
    return models


def update_assessment(session: Session, assessment: Assessment, **kwargs: dict[str, Any]) -> None:
    session.execute(update(DbAssessment).where(DbAssessment.id == assessment.id).values(**kwargs))
    session.commit()


def delete_assessment_by_id(session: Session, _id: UUID) -> None:
    session.execute(delete(DbAssessment).where(DbAssessment.id == _id))
    session.commit()
