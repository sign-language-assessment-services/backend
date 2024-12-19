from datetime import UTC, datetime

from sqlalchemy import delete, update
from sqlalchemy.orm import Session

from app.database.tables.multiple_choices import DbMultipleChoice
from database.utils import table_count
from tests.database.data_inserts import insert_multiple_choice


def test_insert_multiple_choice(db_session: Session) -> None:
    multiple_choice_data = insert_multiple_choice(db_session)

    db_multiple_choice = db_session.get(DbMultipleChoice, multiple_choice_data.get("id"))

    assert table_count(db_session, DbMultipleChoice) == 1
    assert db_multiple_choice.id == multiple_choice_data.get("id")
    assert db_multiple_choice.created_at == multiple_choice_data.get("created_at")


def test_update_multiple_choice(db_session: Session) -> None:
    multiple_choice_data = insert_multiple_choice(db_session)

    db_session.execute(update(DbMultipleChoice).values(created_at=datetime(1970, 1, 1, 0, tzinfo=UTC)))

    db_multiple_choice = db_session.get(DbMultipleChoice, multiple_choice_data.get("id"))
    assert table_count(db_session, DbMultipleChoice) == 1
    assert db_multiple_choice.id == multiple_choice_data.get("id")
    assert db_multiple_choice.created_at != multiple_choice_data.get("created_at")
    assert db_multiple_choice.created_at == datetime(1970, 1, 1, 0, tzinfo=UTC)


def test_delete_multiple_choice(db_session: Session) -> None:
    insert_multiple_choice(db_session)

    db_session.execute(delete(DbMultipleChoice))

    assert table_count(db_session, DbMultipleChoice) == 0
