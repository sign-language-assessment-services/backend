from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.database.tables.assessments import DbAssessment
from app.repositories.assessments import (
    add_assessment, delete_assessment, get_assessment, list_assessments, update_assessment
)
from tests.database.data_inserts import insert_assessment
from tests.database.utils import table_count


def test_add_assessment(db_session: Session) -> None:
    assessment = Assessment(name="Test Assessment")

    add_assessment(db_session, assessment)
    
    result = db_session.get(DbAssessment, assessment.id)
    assert result.id == assessment.id
    assert result.name == assessment.name
    assert table_count(db_session, DbAssessment) == 1


def test_get_assessment_by_id(db_session: Session) -> None:
    assessment_id = insert_assessment(db_session, "Test Assessment").get("id")

    result = get_assessment(db_session, assessment_id)

    assert result.id == assessment_id
    assert result.name == "Test Assessment"
    assert table_count(db_session, DbAssessment) == 1


def test_get_assessment_by_id_returns_none_if_not_found(db_session: Session) -> None:
    result = get_assessment(db_session, uuid4())

    assert result is None


def test_list_no_assessments(db_session: Session) -> None:
    result = list_assessments(db_session)

    assert result == []
    assert table_count(db_session, DbAssessment) == 0


def test_list_multiple_assessments(db_session: Session) -> None:
    for i in range(100):
        insert_assessment(db_session, f"Test Assessment {i}")

    result = list_assessments(db_session)

    assert len(result) == 100
    assert table_count(db_session, DbAssessment) == 100


def test_update_assessment(db_session: Session) -> None:
    assessment_id = insert_assessment(db_session).get("id")

    updated_name = "Updated Assessment"
    update_assessment(db_session, assessment_id, **{"name": updated_name})

    result = db_session.get(DbAssessment, assessment_id)
    assert result.name == updated_name
    assert table_count(db_session, DbAssessment) == 1


def test_delete_assessment(db_session: Session) -> None:
    assessment_id = insert_assessment(db_session).get("id")

    delete_assessment(db_session, assessment_id)

    result = db_session.get(DbAssessment, assessment_id)
    assert result is None
    assert table_count(db_session, DbAssessment) == 0


def test_delete_one_of_two_assessments(db_session: Session) -> None:
    assessment_id = insert_assessment(db_session, "Test 1").get("id")
    insert_assessment(db_session, "Test 2").get("id")

    delete_assessment(db_session, assessment_id)

    result = db_session.get(DbAssessment, assessment_id)
    assert result is None
    assert table_count(db_session, DbAssessment) == 1
