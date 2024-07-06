from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.primer import Primer
from app.database.tables.assessments import DbAssessment
from app.database.tables.primers import DbPrimer


def add_assessment(session: Session, assessment: Assessment) -> None:
    session.add(DbAssessment.from_assessment(assessment))
    session.commit()


def get_assessment_by_id(session: Session, _id: str) -> Assessment:
    result = session.get(DbAssessment, {"id": _id})
    return result.to_assessment()


def list_assessments(session: Session) -> list[AssessmentSummary]:
    result = session.query(DbAssessment).all()
    return [assessment.to_assessment_summary() for assessment in result]


def delete_assessment_by_id(session: Session, _id: str) -> None:
    session.query(DbAssessment).filter_by(id=_id).delete()
    session.commit()


def add_assessment_primer(session: Session, primer: Primer) -> None:
    session.add(DbPrimer.from_primer(primer))
    session.commit()
