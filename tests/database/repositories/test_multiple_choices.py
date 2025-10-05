from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.core.models.choice import AssociatedChoice
from app.core.models.multiple_choice import MultipleChoice
from app.database.exceptions import EntryNotFoundError
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.choices import DbChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from app.repositories.multiple_choices import (
    add_multiple_choice, delete_multiple_choice, get_multiple_choice, list_multiple_choices,
    update_multiple_choice
)
from tests.database.data_inserts import (
    connect_multiple_choice_with_choices, insert_bucket_object, insert_choice,
    insert_multiple_choice
)
from tests.database.utils import table_count


def test_add_multiple_choice_with_choices(db_session: Session) -> None:
    multimedia_file = insert_bucket_object(session=db_session)
    choice_1 = insert_choice(session=db_session, bucket_object_id=multimedia_file.get("id"))
    choice_2 = insert_choice(session=db_session, bucket_object_id=multimedia_file.get("id"))
    choice_3 = insert_choice(session=db_session, bucket_object_id=multimedia_file.get("id"))
    multiple_choice = MultipleChoice(
        choices=[
            AssociatedChoice(**choice_1, is_correct=True, position=1),
            AssociatedChoice(**choice_2, is_correct=False, position=2),
            AssociatedChoice(**choice_3, is_correct=False, position=3)
        ]
    )

    add_multiple_choice(session=db_session, multiple_choice=multiple_choice)

    result = db_session.get(DbMultipleChoice, multiple_choice.id)
    assert result.id == multiple_choice.id
    assert result.created_at == multiple_choice.created_at
    for index, choice in enumerate([choice_1, choice_2, choice_3]):
        assert result.choices[index].id == choice.get("id")
        assert result.associations[index].choice_id == choice.get("id")
        assert result.associations[index].multiple_choice_id == multiple_choice.id
        assert result.associations[index].position == index + 1
    assert result.associations[0].is_correct
    assert not result.associations[1].is_correct
    assert not result.associations[2].is_correct
    assert table_count(db_session, DbMultipleChoice) == 1
    assert table_count(db_session, DbChoice) == 3
    assert table_count(db_session, DbMultipleChoicesChoices) == 3


def test_get_multiple_choice_by_id(db_session: Session) -> None:
    multiple_choice = insert_multiple_choice(session=db_session)

    result = get_multiple_choice(session=db_session, _id=multiple_choice.get("id"))

    assert result.id == multiple_choice.get("id")
    assert result.created_at == multiple_choice.get("created_at")
    assert table_count(db_session, DbMultipleChoice) == 1


def test_get_multiple_choice_by_id_returns_none_if_not_found(db_session: Session) -> None:
    result = get_multiple_choice(session=db_session, _id=uuid4())

    assert result is None


def test_list_no_multiple_choices(db_session: Session) -> None:
    result = list_multiple_choices(session=db_session)

    assert result == []
    assert table_count(db_session, DbMultipleChoice) == 0


def test_list_multiple_multiple_choices(db_session: Session) -> None:
    for _ in range(100):
        insert_multiple_choice(session=db_session)

    result = list_multiple_choices(session=db_session)

    assert len(result) == 100
    assert table_count(db_session, DbMultipleChoice) == 100


def test_update_multiple_choice(db_session: Session) -> None:
    multiple_choice = insert_multiple_choice(session=db_session)

    updated_time = datetime(2001, 1, 1, 1, tzinfo=UTC)
    update_multiple_choice(
        session=db_session,
        _id=multiple_choice.get("id"),
        **{"created_at": updated_time}
    )

    result = db_session.get(DbMultipleChoice, multiple_choice.get("id"))
    assert result.id == multiple_choice.get("id")
    assert result.created_at == updated_time
    assert table_count(db_session, DbMultipleChoice) == 1


def test_delete_multiple_choice(db_session: Session) -> None:
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")

    delete_multiple_choice(session=db_session, _id=multiple_choice_id)

    result = db_session.get(DbMultipleChoice, multiple_choice_id)
    assert result is None
    assert table_count(db_session, DbMultipleChoice) == 0


def test_delete_one_of_two_multiple_choices(db_session: Session) -> None:
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    insert_multiple_choice(session=db_session).get("id")

    delete_multiple_choice(session=db_session, _id=multiple_choice_id)

    result = db_session.get(DbMultipleChoice, multiple_choice_id)
    assert result is None
    assert table_count(db_session, DbMultipleChoice) == 1


def test_delete_not_existing_multiple_choice_should_fail(db_session: Session) -> None:
    with pytest.raises(EntryNotFoundError, match=r"has no entry with id"):
        delete_multiple_choice(session=db_session, _id=uuid4())


def test_delete_multiple_choice_deletes_dependent_choices(db_session: Session) -> None:
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    multimedia_file = insert_bucket_object(session=db_session)
    choice_1 = insert_choice(session=db_session, bucket_object_id=multimedia_file.get("id"))
    choice_2 = insert_choice(session=db_session, bucket_object_id=multimedia_file.get("id"))
    connect_multiple_choice_with_choices(
        session=db_session,
        multiple_choice_id=multiple_choice_id,
        choice_ids=[choice_1.get("id"), choice_2.get("id")]
    )

    delete_multiple_choice(session=db_session, _id=multiple_choice_id)

    result = db_session.get(DbMultipleChoice, multiple_choice_id)
    assert result is None
    assert table_count(db_session, DbMultipleChoice) == 0
    assert table_count(db_session, DbChoice) == 0
    assert table_count(db_session, DbMultipleChoicesChoices) == 0
    assert table_count(db_session, DbBucketObjects) == 1


def test_delete_multiple_choice_does_not_delete_still_used_choices(db_session: Session) -> None:
    multiple_choice_1 = insert_multiple_choice(session=db_session)
    multiple_choice_2 = insert_multiple_choice(session=db_session)
    multimedia_file = insert_bucket_object(session=db_session)
    choice_1 = insert_choice(session=db_session, bucket_object_id=multimedia_file.get("id"))
    choice_2 = insert_choice(session=db_session, bucket_object_id=multimedia_file.get("id"))
    connect_multiple_choice_with_choices(
        session=db_session,
        multiple_choice_id=multiple_choice_1.get("id"),
        choice_ids=[choice_1.get("id")]
    )
    connect_multiple_choice_with_choices(
        session=db_session,
        multiple_choice_id=multiple_choice_2.get("id"),
        choice_ids=[choice_1.get("id"), choice_2.get("id")]
    )

    delete_multiple_choice(session=db_session, _id=multiple_choice_2.get("id"))

    assert db_session.get(DbMultipleChoice, multiple_choice_1.get("id")) is not None
    assert db_session.get(DbMultipleChoice, multiple_choice_2.get("id")) is None
    assert db_session.get(DbChoice, choice_1.get("id")) is not None
    assert db_session.get(DbChoice, choice_2.get("id")) is None
    assert table_count(db_session, DbMultipleChoice) == 1
    assert table_count(db_session, DbChoice) == 1
    assert table_count(db_session, DbMultipleChoicesChoices) == 1
    assert table_count(db_session, DbBucketObjects) == 1
