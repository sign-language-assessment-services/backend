from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.choices import DbChoice
from database.data_inserts import insert_bucket_object
from tests.database.data_inserts import insert_choice


def test_insert_valid_choice(db_session):
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.IMAGE)
    data = insert_choice(
        session=db_session,
        bucket_object_id=bucket_data.get("id")
    )

    data_query = db_session.query(DbChoice)

    assert data_query.count() == 1
    db_choice = data_query.first()
    assert db_choice.id == data.get("id")
    assert db_choice.created_at == data.get("created_at")
    assert db_choice.bucket_object_id == data.get("bucket_object_id")


def test_insert_choice_with_non_existing_bucket_object_fails(db_session: Session) -> None:
    bucket_uuid = uuid4()  # does not exist in database
    data = {
        "id": uuid4(),
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket_object_id": bucket_uuid,
    }

    with pytest.raises(IntegrityError, match=fr'{bucket_uuid}\) is not present in table "bucket_objects"'):
        _add_choices_data(db_session, **data)


def test_insert_choice_with_no_bucket_fails(db_session: Session) -> None:
    data = {
        "id": uuid4(),
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket_object_id": None,
    }

    with pytest.raises(IntegrityError, match=r'"bucket_object_id".*violates not-null constraint'):
        _add_choices_data(db_session, **data)


def test_delete_choice(db_session):
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.IMAGE)
    insert_choice(
        session=db_session,
        bucket_object_id=bucket_data.get("id")
    )

    db_session.query(DbChoice).delete()

    assert db_session.query(DbChoice).count() == 0
    assert db_session.query(DbBucketObjects).count() == 1  # should not be deleted


def _add_choices_data(session, **kwargs) -> None:
    statement = text(
        """
        INSERT INTO Choices(id, created_at, bucket_object_id)
        VALUES (:id, :created_at, :bucket_object_id)
        """
    )
    session.execute(statement, kwargs)
