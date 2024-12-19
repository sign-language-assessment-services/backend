from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.database.tables.multiple_choices import DbMultipleChoice
from tests.database.data_inserts import insert_multiple_choice


def test_insert_multiple_choice(db_session: Session) -> None:
    multiple_choice_data = insert_multiple_choice(db_session)

    data_query = db_session.query(DbMultipleChoice)

    assert data_query.count() == 1
    db_multiple_choice = data_query.first()
    assert db_multiple_choice.id == multiple_choice_data.get("id")
    assert db_multiple_choice.created_at == multiple_choice_data.get("created_at")


def test_update_multiple_choice(db_session: Session) -> None:
    data = insert_multiple_choice(db_session)

    db_session.query(DbMultipleChoice).update({"created_at": datetime(1970, 1, 1, 0, tzinfo=UTC)})

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
