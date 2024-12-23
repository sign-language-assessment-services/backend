from uuid import uuid4

import pytest
from sqlalchemy import delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.choices import DbChoice
from tests.database.data_inserts import insert_bucket_object
from tests.database.utils import table_count
from tests.database.data_inserts import insert_choice


def test_insert_choice(db_session):
    bucket_object_id = insert_bucket_object(session=db_session).get("id")
    choice_data = insert_choice(session=db_session, bucket_object_id=bucket_object_id)

    db_choice = db_session.get(DbChoice, choice_data.get("id"))

    assert db_choice.id == choice_data.get("id")
    assert db_choice.created_at == choice_data.get("created_at")
    assert db_choice.bucket_object_id == choice_data.get("bucket_object_id")
    assert table_count(db_session, DbChoice) == 1


def test_insert_choice_with_non_existing_bucket_object_fails(db_session: Session) -> None:
    bucket_uuid = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{bucket_uuid}\) is not present in table "bucket_objects"'):
        insert_choice(session=db_session, bucket_object_id=bucket_uuid)


def test_insert_choice_with_no_bucket_fails(db_session: Session) -> None:
    bucket_uuid = None

    with pytest.raises(IntegrityError, match=r'"bucket_object_id".*violates not-null constraint'):
        insert_choice(session=db_session, bucket_object_id=bucket_uuid)


def test_update_choice(db_session: Session) -> None:
    bucket_data_id_1 = insert_bucket_object(session=db_session, filename="1").get("id")
    bucket_data_id_2 = insert_bucket_object(session=db_session, filename="2").get("id")
    choice_data = insert_choice(session=db_session, bucket_object_id=bucket_data_id_1)

    db_session.execute(update(DbChoice).values(bucket_object_id=bucket_data_id_2))

    db_choice_object = db_session.get(DbChoice, choice_data.get("id"))
    assert table_count(db_session, DbChoice) == 1
    assert table_count(db_session, DbBucketObjects) == 2
    assert db_choice_object.id == choice_data.get("id")
    assert db_choice_object.bucket_object_id != bucket_data_id_1
    assert db_choice_object.bucket_object_id == bucket_data_id_2


def test_delete_choice(db_session):
    bucket_object_id = insert_bucket_object(session=db_session).get("id")
    insert_choice(session=db_session, bucket_object_id=bucket_object_id)

    db_session.execute(delete(DbChoice))

    assert table_count(db_session, DbChoice) == 0
    assert table_count(db_session, DbBucketObjects) == 1
