import pytest
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

from app.database.tables.assessments import DbAssessment
from tests.database.data_inserts import insert_assessment


def test_insert_assessment(db_session: Session) -> None:
    assessment_data = insert_assessment(db_session)

    data_query = db_session.query(DbAssessment)

    assert data_query.count() == 1
    db_assessment = data_query.first()
    assert db_assessment.id == assessment_data.get("id")
    assert db_assessment.created_at == assessment_data.get("created_at")
    assert db_assessment.name == assessment_data.get("name")


def test_insert_assessment_with_empty_name_fails(db_session: Session) -> None:
    assessment_name = None

    msg = r'null value in column "name" of relation "assessments" violates not-null constraint'
    with pytest.raises(IntegrityError, match=msg):
        insert_assessment(session=db_session, name=assessment_name)


def test_insert_assessment_with_too_long_name_fails(db_session: Session) -> None:
    assessment_name = "x" * 101

    with pytest.raises(DataError, match=r"value too long for type character varying\(100\)"):
        insert_assessment(session=db_session, name=assessment_name)


def test_update_assessment(db_session: Session) -> None:
    assessment_data = insert_assessment(db_session)

    db_session.query(DbAssessment).update({"name": "Updated Assessment"})

    data_query = db_session.query(DbAssessment)
    assert data_query.count() == 1
    db_assessment = data_query.first()
    assert db_assessment.id == assessment_data.get("id")
    assert db_assessment.created_at == assessment_data.get("created_at")
    assert db_assessment.name != assessment_data.get("name")
    assert db_assessment.name == "Updated Assessment"


def test_delete_assessment(db_session: Session) -> None:
    insert_assessment(db_session)

    db_session.query(DbAssessment).delete()

    assert db_session.query(DbAssessment).count() == 0
