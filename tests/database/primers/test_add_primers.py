import re
from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.database.tables.primers import DbPrimer


def test_insert_valid_primer(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "position": 1,
        "assessment_id": "00000000-0000-0000-0000-000000000000",
        "multimedia_file_id": "00000000-0000-0000-0000-000000000001"
    }

    _add_dependency_assessment(db_session)
    _add_dependency_multimedia_file(db_session)
    _add_primer_data(db_session, **data)

    data_query = db_session.query(DbPrimer)
    assert data_query.count() == 1
    assert data_query.first().id == UUID(data.get("id"))
    assert data_query.first().created_at == data.get("created_at")
    assert data_query.first().position == data.get("position")
    assert data_query.first().assessment_id == UUID(data.get("assessment_id"))
    assert data_query.first().multimedia_file_id == UUID(data.get("multimedia_file_id"))


def test_insert_primer_with_missing_assessment_fails(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "position": 1,
        "assessment_id": "00000000-0000-0000-0000-000000000000",
        "multimedia_file_id": "00000000-0000-0000-0000-000000000001"
    }

    _add_dependency_multimedia_file(db_session)

    failure_details = re.compile(
        r'violates foreign key constraint.*not present in table "assessments"',
        re.DOTALL
    )
    with pytest.raises(IntegrityError, match=failure_details):
        _add_primer_data(db_session, **data)


def test_insert_primer_with_missing_multimedia_file_fails(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "position": 1,
        "assessment_id": "00000000-0000-0000-0000-000000000000",
        "multimedia_file_id": "00000000-0000-0000-0000-000000000001"
    }

    _add_dependency_assessment(db_session)

    failure_details = re.compile(
        r'violates foreign key constraint.*not present in table "multimedia_files"',
        re.DOTALL
    )
    with pytest.raises(IntegrityError, match=failure_details):
        _add_primer_data(db_session, **data)


def _add_primer_data(session, **kwargs) -> None:
    statement = text(
        """
        INSERT INTO primers(id, created_at, position, assessment_id, multimedia_file_id)
        VALUES (:id, :created_at, :position, :assessment_id, :multimedia_file_id)
        """
    )
    session.execute(statement, kwargs)


def _add_dependency_assessment(session) -> None:
    assessment = {
        "id": "00000000-0000-0000-0000-000000000000",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Test Assessment"
    }
    assessment_statement = text(
        """
        INSERT INTO assessments(id, created_at, name)
        VALUES (:id, :created_at, :name)
        """
    )
    session.execute(assessment_statement, assessment)


def _add_dependency_multimedia_file(session) -> None:
    multimedia_file = {
        "id": "00000000-0000-0000-0000-000000000001",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket": "testportal",
        "key": "test.mpeg",
        "mediatype": "VIDEO"
    }
    multimedia_file_statement = text(
        """
        INSERT INTO multimedia_files(id, created_at, bucket, key, mediatype)
        VALUES (:id, :created_at, :bucket, :key, :mediatype)
        """
    )
    session.execute(multimedia_file_statement, multimedia_file)
