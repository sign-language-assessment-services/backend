from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.choices import DbChoice
from database.data_inserts import insert_bucket_object
from tests.database.data_inserts import insert_choice


def test_insert_choice(db_session):
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.IMAGE)
    choice_data = insert_choice(session=db_session, bucket_object_id=bucket_data.get("id"))

    data_query = db_session.query(DbChoice)

    assert data_query.count() == 1
    db_choice = data_query.first()
    assert db_choice.id == choice_data.get("id")
    assert db_choice.created_at == choice_data.get("created_at")
    assert db_choice.bucket_object_id == choice_data.get("bucket_object_id")


def test_insert_choice_with_non_existing_bucket_object_fails(db_session: Session) -> None:
    bucket_uuid = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{bucket_uuid}\) is not present in table "bucket_objects"'):
        insert_choice(session=db_session, bucket_object_id=bucket_uuid)


def test_insert_choice_with_no_bucket_fails(db_session: Session) -> None:
    bucket_uuid = None

    with pytest.raises(IntegrityError, match=r'"bucket_object_id".*violates not-null constraint'):
        insert_choice(session=db_session, bucket_object_id=bucket_uuid)


def test_update_choice(db_session: Session) -> None:
    bucket_data_1 = insert_bucket_object(session=db_session, content_type=MediaType.IMAGE, key_suffix="1")
    bucket_data_2 = insert_bucket_object(session=db_session, content_type=MediaType.IMAGE, key_suffix="2")
    choice_data = insert_choice(session=db_session, bucket_object_id=bucket_data_1.get("id"))

    db_session.query(DbChoice).update({"bucket_object_id": bucket_data_2.get("id")})

    data_query = db_session.query(DbChoice)
    assert data_query.count() == 1
    db_bucket_object = data_query.first()
    assert db_bucket_object.id == choice_data.get("id")
    assert db_bucket_object.bucket_object_id != bucket_data_1.get("id")
    assert db_bucket_object.bucket_object_id == bucket_data_2.get("id")


def test_delete_choice(db_session):
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.IMAGE)
    insert_choice(session=db_session, bucket_object_id=bucket_data.get("id"))

    db_session.query(DbChoice).delete()

    assert db_session.query(DbChoice).count() == 0
    assert db_session.query(DbBucketObjects).count() == 1
