from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.core.models.primer import Primer
from app.database.tables.assessments import DbAssessment
from app.database.tables.primers import DbPrimer
from app.mappers.assessment_mapper import AssessmentMapper


def add_assessment(session: Session, assessment: Assessment) -> None:
    session.add(DbAssessment.from_assessment(assessment))
    session.commit()


def get_assessment_by_id(session: Session, _id: str) -> Assessment | None:
    result = session.get(DbAssessment, {"id": _id})
    if result:
        return AssessmentMapper.db_to_domain(result)
    return None


def list_assessments(session: Session) -> list[Assessment]:
    results = session.query(DbAssessment).all()
    return [AssessmentMapper.db_to_domain(result) for result in results]


def delete_assessment_by_id(session: Session, _id: str) -> None:
    session.query(DbAssessment).filter_by(id=_id).delete()
    session.commit()


def add_assessment_primer(session: Session, primer: Primer) -> None:
    session.add(DbPrimer.from_primer(primer))
    session.commit()
