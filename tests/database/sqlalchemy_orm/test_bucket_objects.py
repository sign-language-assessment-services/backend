import pytest
from sqlalchemy import delete, update
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from database.utils import table_count
from database.data_inserts import insert_bucket_object


@pytest.mark.parametrize("media_type", [MediaType.VIDEO, MediaType.IMAGE])
def test_insert_bucket_object(media_type: MediaType, db_session: Session) -> None:
    bucket_object_data = insert_bucket_object(db_session, media_type)

    db_bucket_object = db_session.get(DbBucketObjects, bucket_object_data.get("id"))

    assert table_count(db_session, DbBucketObjects) == 1
    assert db_bucket_object.id == bucket_object_data.get("id")
    assert db_bucket_object.created_at == bucket_object_data.get("created_at")
    assert db_bucket_object.bucket == bucket_object_data.get("bucket")
    assert db_bucket_object.key == bucket_object_data.get("key")
    assert db_bucket_object.media_type == media_type


def test_insert_bucket_object_with_too_long_bucket_name(db_session: Session) -> None:
    bucket_name = "x" * 64

    with pytest.raises(DataError, match=r'value too long for type character varying\(63\)'):
        insert_bucket_object(db_session, MediaType.VIDEO, bucket_name=bucket_name)


def test_insert_bucket_object_with_too_long_key_name(db_session: Session) -> None:
    filename = "x" * 1025

    with pytest.raises(DataError, match=r'value too long for type character varying\(1024\)'):
        insert_bucket_object(db_session, filename=filename)


def test_update_bucket_object(db_session: Session) -> None:
    bucket_object_data = insert_bucket_object(db_session)

    updated_bucket = "updated_bucket"
    updated_key = "updated_key"
    db_session.execute(update(DbBucketObjects).values(bucket=updated_bucket, key=updated_key))

    db_bucket_object = db_session.get(DbBucketObjects, bucket_object_data.get("id"))
    assert db_bucket_object.bucket == updated_bucket
    assert db_bucket_object.key == updated_key
    assert table_count(db_session, DbBucketObjects) == 1


def test_delete_bucket_object(db_session):
    insert_bucket_object(db_session)

    db_session.execute(delete(DbBucketObjects))

    assert table_count(db_session, DbBucketObjects) == 0
