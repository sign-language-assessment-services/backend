from datetime import UTC, datetime, timezone
from uuid import UUID

import pytest
import pytz
from sqlalchemy import text
from sqlalchemy.exc import DataError

from app.database.tables.assessments import DbAssessment


def test_insert_correct_assessment(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Test Assessment"
    }

    _add_assessment_data(db_session, **data)

    data_query = db_session.query(DbAssessment)
    assert data_query.count() == 1
    assert data_query.first().id == UUID(data.get("id"))
    assert data_query.first().created_at == data.get("created_at")
    assert data_query.first().name == data.get("name")


def test_insert_assessment_without_timezone_returns_utc(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12),
        "name": "Test Assessment"
    }

    _add_assessment_data(db_session, **data)

    data_query = db_session.query(DbAssessment)
    assert data_query.first().created_at == datetime(2000, 1, 1, 12, tzinfo=UTC)


def test_insert_assessment_with_different_timezone_saves_it_as_utc(db_session):
    berlin_time = pytz.timezone("Europe/Berlin").localize(datetime(2000, 1, 1, 12))
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": berlin_time,
        "name": "Test Assessment"
    }

    _add_assessment_data(db_session, **data)

    data_query = db_session.query(DbAssessment)
    assert data_query.first().created_at == berlin_time
    assert data_query.first().created_at.tzinfo == timezone.utc
    assert data_query.first().created_at == datetime(2000, 1, 1, 11, tzinfo=UTC)


def test_insert_assessment_with_too_long_name(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "x" * 101
    }

    with pytest.raises(DataError, match=r"value too long for type character varying\(100\)"):
        _add_assessment_data(db_session, **data)


def test_insert_assessment_with_wrong_uuid(db_session):
    data = {
        "id": "this_isn-t_av-alid-uuid-is_not_good.",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Test Assessment"
    }

    with pytest.raises(DataError, match=r"invalid input syntax for type uuid"):
        _add_assessment_data(db_session, **data)


def test_insert_assessment_with_wrong_date(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": "2000-1-1 25:00",
        "name": "Test Assessment"
    }

    with pytest.raises(DataError, match=r"date/time field value out of range"):
        _add_assessment_data(db_session, **data)


def _add_assessment_data(session, **kwargs) -> None:
    statement = text(
        """
        INSERT INTO assessments(id, created_at, name)
        VALUES (:id, :created_at, :name)
        """
    )
    session.execute(statement, kwargs)
