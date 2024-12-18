from datetime import UTC, datetime, timezone
from uuid import uuid4

import pytest
import pytz
from sqlalchemy import text
from sqlalchemy.exc import DataError, IntegrityError

from app.database.tables.assessments import DbAssessment
from tests.database.data_inserts import insert_assessment


def test_insert_valid_assessment(db_session) -> None:
    data = insert_assessment(db_session)

    data_query = db_session.query(DbAssessment)

    assert data_query.count() == 1
    db_assessment = data_query.first()
    assert db_assessment.id == data.get("id")
    assert db_assessment.created_at == data.get("created_at")
    assert db_assessment.name == data.get("name")


def test_insert_assessment_without_timezone_returns_utc(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12),
        "name": "Test Assessment"
    }

    _add_assessment_data(db_session, **data)

    data_query = db_session.query(DbAssessment)
    assert data_query.first().created_at == datetime(2000, 1, 1, 12, tzinfo=UTC)



def test_insert_assessment_with_different_timezone_saves_it_as_utc(db_session) -> None:
    berlin_time = pytz.timezone("Europe/Berlin").localize(datetime(2000, 1, 1, 12))
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": berlin_time,
        "name": "Test Assessment"
    }

    _add_assessment_data(db_session, **data)

    data_query = db_session.query(DbAssessment)
    db_assessment = data_query.first()
    assert db_assessment.created_at == berlin_time
    assert db_assessment.created_at.tzinfo == timezone.utc
    assert db_assessment.created_at == datetime(2000, 1, 1, 11, tzinfo=UTC)


def test_insert_two_assessments_with_same_id_will_fail(db_session) -> None:
    any_uuid = uuid4()
    data_1 = {
        "id": any_uuid,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Foo"
    }
    data_2 = {
        "id": any_uuid,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Bar"
    }

    _add_assessment_data(db_session, **data_1)

    with pytest.raises(IntegrityError, match=r"duplicate key value violates unique constraint"):
        _add_assessment_data(db_session, **data_2)


def test_insert_assessment_with_too_long_name(db_session) -> None:
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "x" * 101
    }

    with pytest.raises(DataError, match=r"value too long for type character varying\(100\)"):
        _add_assessment_data(db_session, **data)


def test_insert_assessment_with_wrong_uuid(db_session) -> None:
    data = {
        "id": "this_isn-t_av-alid-uuid-is_not_good.",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Test Assessment"
    }

    with pytest.raises(DataError, match=r"invalid input syntax for type uuid"):
        _add_assessment_data(db_session, **data)


def test_insert_assessment_with_wrong_date(db_session) -> None:
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": "2000-1-1 25:00",
        "name": "Test Assessment"
    }

    with pytest.raises(DataError, match=r"date/time field value out of range"):
        _add_assessment_data(db_session, **data)


def test_update_assessment(db_session) -> None:
    data = insert_assessment(db_session)

    db_session.query(DbAssessment).update({"name": "Updated Assessment"})

    data_query = db_session.query(DbAssessment)
    assert data_query.count() == 1
    db_assessment = data_query.first()
    assert db_assessment.id == data.get("id")
    assert db_assessment.created_at == data.get("created_at")
    assert db_assessment.name == "Updated Assessment"


def test_delete_assessment(db_session) -> None:
    insert_assessment(db_session)

    db_session.query(DbAssessment).delete()

    assert db_session.query(DbAssessment).count() == 0


def _add_assessment_data(session, **kwargs) -> None:
    statement = text(
        """
        INSERT INTO assessments(id, created_at, name)
        VALUES (:id, :created_at, :name)
        """
    )
    session.execute(statement, kwargs)
