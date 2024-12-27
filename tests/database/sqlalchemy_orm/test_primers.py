from uuid import uuid4

import pytest
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from database.utils import table_count
from database.data_inserts import insert_bucket_object, insert_primer


def test_insert_primer(db_session: Session) -> None:
    bucket_data = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO)

    primer_data = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))

    db_primer = db_session.get(DbPrimer, primer_data.get("id"))
    assert table_count(db_session, DbPrimer) == 1
    assert db_primer.id == primer_data.get("id")
    assert db_primer.bucket_object_id == primer_data.get("bucket_object_id")


def test_insert_primer_with_non_existing_bucket_object_fails(db_session):
    bucket_id = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{bucket_id}.*not present in table "bucket_objects"'):
        insert_primer(session=db_session, bucket_object_id=bucket_id)


def test_update_primer(db_session: Session) -> None:
    bucket_object_data_1 = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO, filename="1")
    primer_data = insert_primer(session=db_session, bucket_object_id=bucket_object_data_1.get("id"))

    bucket_object_data_2 = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO, filename="2")
    db_session.execute(update(DbPrimer).values(bucket_object_id=bucket_object_data_2.get("id")))

    db_primer = db_session.get(DbPrimer, primer_data.get("id"))
    assert table_count(db_session, DbPrimer) == 1
    assert db_primer.id == primer_data.get("id")
    assert db_primer.bucket_object_id != bucket_object_data_1.get("id")
    assert db_primer.bucket_object_id == bucket_object_data_2.get("id")


def test_delete_primers(db_session):
    bucket_data = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO)
    insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))

    db_primer = db_session.scalar(select(DbPrimer))
    db_session.delete(db_primer)

    assert table_count(db_session, DbPrimer) == 0
    assert table_count(db_session, DbTask) == 0
    assert table_count(db_session, DbBucketObjects) == 1
