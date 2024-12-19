import pytest
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from tests.database.data_inserts import insert_bucket_object


@pytest.mark.parametrize("content_type", [MediaType.VIDEO, MediaType.IMAGE])
def test_insert_bucket_object(content_type: MediaType, db_session: Session) -> None:
    bucket_object_data = insert_bucket_object(db_session, content_type)

    data_query = db_session.query(DbBucketObjects)

    assert data_query.count() == 1
    db_bucket_object = data_query.first()
    assert db_bucket_object.id == bucket_object_data.get("id")
    assert db_bucket_object.created_at == bucket_object_data.get("created_at")
    assert db_bucket_object.bucket == bucket_object_data.get("bucket")
    assert db_bucket_object.key == bucket_object_data.get("key")
    assert db_bucket_object.content_type == content_type


def test_insert_bucket_object_with_too_long_bucket_name(db_session: Session) -> None:
    bucket_name = "x" * 64

    with pytest.raises(DataError, match=r'value too long for type character varying\(63\)'):
        insert_bucket_object(db_session, MediaType.VIDEO, bucket_name=bucket_name)


def test_insert_bucket_object_with_too_long_key_name(db_session: Session) -> None:
    bucket_key_suffix = "x" * 1016  # 1025 - len("test.mpeg")

    with pytest.raises(DataError, match=r'value too long for type character varying\(1024\)'):
        insert_bucket_object(db_session, MediaType.VIDEO, key_suffix=bucket_key_suffix)


def test_update_bucket_object(db_session: Session) -> None:
    bucket_object_data = insert_bucket_object(db_session, MediaType.VIDEO)

    db_session.query(DbBucketObjects).update({"bucket": "updated_bucket", "key": "updated_key"})

    data_query = db_session.query(DbBucketObjects)
    assert data_query.count() == 1
    db_bucket_object = data_query.first()
    assert db_bucket_object.id == bucket_object_data.get("id")
    assert db_bucket_object.created_at == bucket_object_data.get("created_at")
    assert db_bucket_object.bucket == "updated_bucket"
    assert db_bucket_object.key == "updated_key"
    assert db_bucket_object.content_type == MediaType.VIDEO


def test_delete_bucket_object(db_session):
    insert_bucket_object(db_session, MediaType.IMAGE)

    db_session.query(DbBucketObjects).delete()

    assert db_session.query(DbBucketObjects).count() == 0
