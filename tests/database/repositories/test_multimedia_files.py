from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.bucket_objects import DbBucketObjects
from app.repositories.multimedia_files import (
    add_multimedia_file, delete_multimedia_file, get_multimedia_file, list_multimedia_files,
    update_multimedia_file
)
from tests.database.data_inserts import insert_bucket_object
from tests.database.utils import table_count


@pytest.mark.parametrize("_type", [MediaType.VIDEO, MediaType.IMAGE])
def test_add_multimedia_file(db_session: Session, _type: MediaType) -> None:
    multimedia_file = MultimediaFile(
        location=MinioLocation(bucket="testportal", key="1234"),
        media_type=_type
    )

    add_multimedia_file(db_session, multimedia_file)

    result = db_session.get(DbBucketObjects, multimedia_file.id)
    assert result.bucket == "testportal"
    assert result.key == "1234"
    assert result.media_type == _type
    assert table_count(db_session, DbBucketObjects) == 1


def test_get_multimedia_file_by_id(db_session: Session) -> None:
    name = f"{uuid4()}.mpg"
    video_id = insert_bucket_object(db_session, filename=name).get("id")
    
    result = get_multimedia_file(db_session, video_id)

    assert result.id == video_id
    assert result.location.key == name
    assert table_count(db_session, DbBucketObjects) == 1


def test_get_multimedia_file_by_id_returns_none_if_not_found(db_session: Session) -> None:
    result = get_multimedia_file(db_session, uuid4())

    assert result is None


def test_list_no_multimedia_files(db_session: Session) -> None:
    result = list_multimedia_files(db_session)

    assert result == []
    assert table_count(db_session, DbBucketObjects) == 0


def test_list_multiple_multimedia_files(db_session: Session) -> None:
    for i in range(100):
        insert_bucket_object(db_session, filename=f"{i}.mpg")

    result = list_multimedia_files(db_session)

    assert len(result) == 100
    assert table_count(db_session, DbBucketObjects) == 100


def test_update_multimedia_file(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session, filename="1.mpg").get("id")
    
    updated_filename = "2.mpg"
    update_multimedia_file(db_session, video_id, **{"key": updated_filename})
    
    result = db_session.get(DbBucketObjects, video_id)
    assert result.key == updated_filename
    assert table_count(db_session, DbBucketObjects) == 1


def test_delete_multimedia_file(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session, filename="1.mpg").get("id")
    
    delete_multimedia_file(db_session, video_id)
    
    result = db_session.get(DbBucketObjects, video_id)
    assert result is None
    assert table_count(db_session, DbBucketObjects) == 0


def test_delete_one_of_two_multimedia_files(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session, filename="1.mpg").get("id")
    insert_bucket_object(db_session, filename="2.mpg")

    delete_multimedia_file(db_session, video_id)

    result = db_session.get(DbBucketObjects, video_id)
    assert result is None
    assert table_count(db_session, DbBucketObjects) == 1
