from datetime import datetime, timedelta

import pytest
from sqlalchemy import text

from app.core.models.media_types import MediaType
from app.core.models.multimedia_file import MultimediaFile
from app.repositories.multimedia_files import (add_multimedia_file, delete_multimedia_file_by_id,
                                               get_multimedia_file_by_id, list_multimedia_files)


@pytest.mark.parametrize("media_type", [MediaType.VIDEO, MediaType.IMAGE])
def test_add_multimedia_file(media_type, db_session):
    multimedia_file = MultimediaFile(
        bucket="testportal",
        key="1234",
        type=media_type,
        url="http://my-media"
    )
    add_multimedia_file(db_session, multimedia_file)

    db_multimedia_file = db_session.execute(text("SELECT * FROM multimedia_files")).fetchone()

    assert db_multimedia_file[2] == "testportal"
    assert db_multimedia_file[3] == "1234"


def test_get_multimedia_file_by_id(db_session, insert_multimedia_file):
    insert_multimedia_file(1)
    assert get_multimedia_file_by_id(db_session, "test_id-1") == MultimediaFile(
        bucket="testportal",
        key="001",
        type=None,
        url=""
    )


def test_list_no_multimedia_files(db_session):
    result = list_multimedia_files(db_session)
    assert result == []


def test_list_one_multimedia_file(db_session, insert_multimedia_file):
    insert_multimedia_file(1)

    result = list_multimedia_files(db_session)

    assert result == [
        MultimediaFile(
            bucket="testportal",
            key="001",
            type=None,
            url=""
        )
    ]


def test_list_multiple_assessments(db_session, insert_multimedia_file):
    insert_multimedia_file(100)

    result = list_multimedia_files(db_session)

    assert len(result) == 100


def test_delete_one_of_two_multimedia_files(db_session, insert_multimedia_file):
    insert_multimedia_file(2)

    delete_multimedia_file_by_id(db_session, "test_id-1")

    assert get_multimedia_file_by_id(db_session, "test_id-2")
    with pytest.raises(AttributeError):
        get_multimedia_file_by_id(db_session, "test_id-1")
