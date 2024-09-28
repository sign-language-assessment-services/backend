import re
from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.database.tables.choices import DbChoice
from database.dependencies import EXERCISE_ID, add_exercise, add_multimedia_file


def test_insert_valid_choice(db_session):
    multimedia_file_id = "00000000-0000-0000-aaaa-000000000000"
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "is_correct": True,
        "exercise_id": EXERCISE_ID,
        "multimedia_file_id": multimedia_file_id
    }

    add_exercise(db_session, with_dependencies=True)
    add_multimedia_file(db_session, _id=multimedia_file_id)
    _add_choices_data(db_session, **data)

    data_query = db_session.query(DbChoice)
    assert data_query.count() == 1
    assert data_query.first().id == UUID(data.get("id"))
    assert data_query.first().created_at == data.get("created_at")
    assert data_query.first().is_correct == data.get("is_correct")
    assert data_query.first().exercise_id == UUID(data.get("exercise_id"))
    assert data_query.first().multimedia_file_id == UUID(data.get("multimedia_file_id"))


def test_insert_choice_with_missing_exercise_fails(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "is_correct": True,
        "exercise_id": EXERCISE_ID,
        "multimedia_file_id": "00000000-0000-0000-aaaa-000000000000"
    }

    add_multimedia_file(db_session, _id=data.get("multimedia_file_id"))

    failure_details = re.compile(
        r'violates foreign key constraint.*not present in table "exercises"',
        re.DOTALL
    )
    with pytest.raises(IntegrityError, match=failure_details):
        _add_choices_data(db_session, **data)


def test_insert_choice_with_missing_multimedia_file_fails(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "is_correct": True,
        "exercise_id": EXERCISE_ID,
        "multimedia_file_id": "00000000-0000-0000-aaaa-000000000000"
    }

    add_exercise(db_session, with_dependencies=True)
    failure_details = re.compile(
        r'violates foreign key constraint.*not present in table "multimedia_files"',
        re.DOTALL
    )
    with pytest.raises(IntegrityError, match=failure_details):
        _add_choices_data(db_session, **data)


def _add_choices_data(session, **kwargs) -> None:
    statement = text(
        """
        INSERT INTO Choices(id, created_at, is_correct, exercise_id, multimedia_file_id)
        VALUES (:id, :created_at, :is_correct, :exercise_id, :multimedia_file_id)
        """
    )
    session.execute(statement, kwargs)
