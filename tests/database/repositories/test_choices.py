from unittest.mock import patch
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

import app.mappers.choice_mapper as choice_mapper_module
from app.core.models.choice import Choice
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.database.exceptions import EntryNotFoundError
from app.database.tables.choices import DbChoice
from app.mappers.choice_mapper import _get_correct_choice_from_association_table
from app.repositories.choices import (
    add_choice, delete_choice, get_choice, list_choices, update_choice
)
from tests.database.data_inserts import insert_bucket_object, insert_choice
from tests.database.utils import table_count


def test_add_choice(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    video = MultimediaFile(
        id=video_id,
        location=MinioLocation(bucket="test-bucket", key="test.mpg"),
        media_type=MediaType.VIDEO
    )
    choice = Choice(content=video)

    add_choice(session=db_session, choice=choice)
    
    result = db_session.get(DbChoice, choice.id)
    assert result.id == choice.id
    assert result.created_at == choice.created_at
    assert result.bucket_object_id == video_id
    assert table_count(db_session, DbChoice) == 1


@patch.object(choice_mapper_module, _get_correct_choice_from_association_table.__name__, return_value=True)
def test_get_choice_by_id(_, db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    choice = insert_choice(session=db_session, bucket_object_id=video_id)

    result = get_choice(session=db_session, _id=choice.get("id"))

    assert result.id == choice.get("id")
    assert result.created_at == choice.get("created_at")
    assert result.content.id == video_id
    assert table_count(db_session, DbChoice) == 1


def test_get_choice_by_id_returns_none_if_not_found(db_session: Session) -> None:
    result = get_choice(session=db_session, _id=uuid4())

    assert result is None


def test_list_no_choices(db_session: Session) -> None:
    result = list_choices(session=db_session)

    assert result == []
    assert table_count(db_session, DbChoice) == 0


@patch.object(choice_mapper_module, _get_correct_choice_from_association_table.__name__, return_value=True)
def test_list_multiple_choices(_, db_session: Session) -> None:
    for _ in range(100):
        video_id = insert_bucket_object(session=db_session).get("id")
        insert_choice(session=db_session, bucket_object_id=video_id)

    result = list_choices(session=db_session)

    assert len(result) == 100
    assert table_count(db_session, DbChoice) == 100


def test_update_choice(db_session: Session) -> None:
    video_id_1 = insert_bucket_object(session=db_session).get("id")
    choice = insert_choice(session=db_session, bucket_object_id=video_id_1)
    video_id_2 = insert_bucket_object(session=db_session).get("id")

    update_choice(
        session=db_session,
        _id=choice.get("id"),
        **{"bucket_object_id": video_id_2}
    )

    result = db_session.get(DbChoice, choice.get("id"))
    assert result.id == choice.get("id")
    assert result.created_at == choice.get("created_at")
    assert result.bucket_object_id == video_id_2
    assert table_count(db_session, DbChoice) == 1


def test_delete_choice(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    choice_id = insert_choice(session=db_session, bucket_object_id=video_id).get("id")

    delete_choice(session=db_session, _id=choice_id)

    result = db_session.get(DbChoice, choice_id)
    assert result is None
    assert table_count(db_session, DbChoice) == 0


def test_delete_one_of_two_choices(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    choice_id = insert_choice(session=db_session, bucket_object_id=video_id).get("id")
    insert_choice(session=db_session, bucket_object_id=video_id).get("id")

    delete_choice(session=db_session, _id=choice_id)

    result = db_session.get(DbChoice, choice_id)
    assert result is None
    assert table_count(db_session, DbChoice) == 1


def test_delete_not_existing_choice_should_fail(db_session: Session) -> None:
    with pytest.raises(EntryNotFoundError, match=r"has no entry with id"):
        delete_choice(session=db_session, _id=uuid4())
