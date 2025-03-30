from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.primer import Primer
from app.database.exceptions import EntryNotFoundError
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from app.repositories.primers import (
    add_primer, delete_primer, get_primer, list_primers, update_primer
)
from tests.database.data_inserts import insert_bucket_object, insert_primer
from tests.database.utils import table_count


def test_add_primer(db_session: Session) -> None:
    video = insert_bucket_object(session=db_session)
    primer = Primer(
        content=MultimediaFile(
            id=video.get("id"),
            location=MinioLocation(
                bucket=video.get("bucket"),
                key=video.get("key")
            ),
            media_type=video.get("media_type")
        )
    )

    add_primer(session=db_session, primer=primer)

    result = db_session.get(DbPrimer, primer.id)
    assert result.id == primer.id
    assert result.bucket_object_id == primer.content.id
    assert table_count(db_session, DbPrimer) == 1
    assert table_count(db_session, DbTask) == 1


def test_get_primer_by_id(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    primer = insert_primer(session=db_session, bucket_object_id=video_id)

    result = get_primer(session=db_session, _id=primer.get("id"))

    assert result.id == primer.get("id")
    assert result.content.id == video_id
    assert table_count(db_session, DbPrimer) == 1
    assert table_count(db_session, DbTask) == 1


def test_get_primer_by_id_returns_none_if_not_found(db_session: Session) -> None:
    result = get_primer(session=db_session, _id=uuid4())

    assert result is None


def test_list_no_primers(db_session: Session) -> None:
    result = list_primers(session=db_session)

    assert result == []
    assert table_count(db_session, DbPrimer) == 0
    assert table_count(db_session, DbTask) == 0


def test_list_multiple_primers(db_session: Session) -> None:
    for i in range(100):
        video_id = insert_bucket_object(session=db_session).get("id")
        insert_primer(session=db_session, bucket_object_id=video_id)

    result = list_primers(session=db_session)

    assert len(result) == 100
    assert table_count(db_session, DbPrimer) == 100
    assert table_count(db_session, DbTask) == 100


def test_update_primer(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    primer_id = insert_primer(session=db_session, bucket_object_id=video_id).get("id")

    new_video_id = insert_bucket_object(session=db_session).get("id")
    update_primer(
        session=db_session,
        _id=primer_id,
        **{"bucket_object_id": new_video_id}
    )

    result = db_session.get(DbPrimer, primer_id)
    assert result.id == primer_id
    assert result.bucket_object_id == new_video_id
    assert table_count(db_session, DbPrimer) == 1
    assert table_count(db_session, DbTask) == 1


def test_delete_primer(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    primer_id = insert_primer(session=db_session, bucket_object_id=video_id).get("id")

    delete_primer(session=db_session, _id=primer_id)

    result = db_session.get(DbPrimer, primer_id)
    assert result is None
    assert table_count(db_session, DbPrimer) == 0
    assert table_count(db_session, DbTask) == 0


def test_delete_one_of_two_primers(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    primer_id = insert_primer(session=db_session, bucket_object_id=video_id).get("id")
    insert_primer(session=db_session, bucket_object_id=video_id).get("id")

    delete_primer(session=db_session, _id=primer_id)

    result = db_session.get(DbPrimer, primer_id)
    assert result is None
    assert table_count(db_session, DbPrimer) == 1
    assert table_count(db_session, DbTask) == 1


def test_delete_not_existing_primer_should_fail(db_session: Session) -> None:
    with pytest.raises(EntryNotFoundError, match=r"has no entry with id"):
        delete_primer(session=db_session, _id=uuid4())
