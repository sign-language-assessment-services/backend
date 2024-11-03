from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.database.tables.assessments import DbAssessment
from app.mappers.assessment_mapper import AssessmentMapper


def add_assessment(session: Session, assessment: Assessment) -> None:
    db_model = AssessmentMapper.domain_to_db(assessment)
    session.add(db_model)
    session.commit()
    return None


def get_assessment_by_id(session: Session, _id: UUID) -> Assessment | None:
    result = session.get(DbAssessment, {"id": _id})
    if result:
        model = AssessmentMapper.db_to_domain(result)
        return model
    return None


def list_assessments(session: Session) -> list[Assessment]:
    results = session.query(DbAssessment).all()
    models = [AssessmentMapper.db_to_domain(result) for result in results]
    return models


def update_assessment(session: Session, assessment: Assessment, **kwargs: dict[str, Any]) -> None:
    session.query(DbAssessment).filter_by(id=assessment.id).update(kwargs)
    session.commit()
    return None


def delete_assessment_by_id(session: Session, _id: UUID) -> None:
    session.query(DbAssessment).filter_by(id=_id).delete()
    session.commit()
    return None
