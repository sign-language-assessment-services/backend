from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.tables.multiple_choices import DbMultipleChoice
from tests.database.data_inserts import insert_multiple_choice


def test_insert_valid_multiple_choice(db_session: Session) -> None:
    data = insert_multiple_choice(db_session)

    data_query = db_session.query(DbMultipleChoice)

    assert data_query.count() == 1
    db_multiple_choice = data_query.first()
    assert db_multiple_choice.id == data.get("id")
    assert db_multiple_choice.created_at == data.get("created_at")


def test_insert_two_multiple_choices_with_same_id_will_fail(db_session: Session) -> None:
    any_uuid = uuid4()
    data_1 = {
        "id": any_uuid,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
    }
    data_2 = {
        "id": any_uuid,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
    }

    _add_multiple_choice_data(db_session, **data_1)

    with pytest.raises(IntegrityError, match=r"duplicate key value violates unique constraint"):
        _add_multiple_choice_data(db_session, **data_2)


def test_update_multiple_choice(db_session: Session) -> None:
    data = insert_multiple_choice(db_session)

    db_session.query(DbMultipleChoice).update(
        {
            "created_at": datetime(1970, 1, 1, 0, tzinfo=UTC)
        }
    )

    data_query = db_session.query(DbMultipleChoice)
    assert data_query.count() == 1
    db_multiple_choice = data_query.first()
    assert db_multiple_choice.id == data.get("id")
    assert db_multiple_choice.created_at != data.get("created_at")
    assert db_multiple_choice.created_at == datetime(1970, 1, 1, 0, tzinfo=UTC)


def test_delete_multiple_choice(db_session: Session) -> None:
    insert_multiple_choice(db_session)

    db_session.query(DbMultipleChoice).delete()

    assert db_session.query(DbMultipleChoice).count() == 0


def _add_multiple_choice_data(session, **kwargs) -> None:
    statement = text(
        """
        INSERT INTO multiple_choices(id, created_at)
        VALUES (:id, :created_at)
        """
    )
    session.execute(statement, kwargs)
