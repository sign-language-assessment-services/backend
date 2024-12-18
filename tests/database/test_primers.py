from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from tests.database.data_inserts import insert_bucket_object, insert_primer


def test_insert_valid_primer(db_session: Session) -> None:
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    primer_data = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))

    data_query = db_session.query(DbPrimer)

    assert data_query.count() == 1
    db_primer = data_query.first()
    assert db_primer.id == primer_data.get("id")
    assert db_primer.bucket_object_id == primer_data.get("bucket_object_id")


def test_insert_primer_with_non_existing_bucket_object_fails(db_session):
    bucket_id = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{bucket_id}.*not present in table "bucket_objects"'):
        insert_primer(session=db_session, bucket_object_id=bucket_id)


def test_delete_primers(db_session):
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))

    db_primer = db_session.scalar(select(DbPrimer))
    db_session.delete(db_primer)

    assert db_session.query(DbPrimer).count() == 0
    assert db_session.query(DbTask).count() == 0  # Task should be deleted as well
    assert db_session.query(DbBucketObjects).count() == 1  # Bucket object should not be deleted
