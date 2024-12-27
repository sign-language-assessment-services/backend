from sqlalchemy.orm import Session

from app.core.models.choice import Choice
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.choices import DbChoice
from app.repositories.choices import (
    add_choice, delete_choice, get_choice, list_choices, update_choice
)
from database.data_inserts import insert_bucket_object, insert_choice
from database.utils import table_count


def test_add_choice(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    video = MultimediaFile(
        id=video_id,
        location=MinioLocation(bucket="test-bucket", key="test.mpg"),
        media_type=MediaType.VIDEO
    )
    choice = Choice(content=video)

    add_choice(db_session, choice)
    
    result = db_session.get(DbChoice, choice.id)
    assert result.id == choice.id
    assert result.bucket_object_id == video_id
    assert table_count(db_session, DbChoice) == 1


def test_get_choice_by_id(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    choice_id = insert_choice(db_session, video_id).get("id")

    result = get_choice(db_session, choice_id)

    assert result.id == choice_id
    assert result.content.id == video_id
    assert table_count(db_session, DbChoice) == 1


def test_list_no_choices(db_session: Session) -> None:
    result = list_choices(db_session)

    assert result == []
    assert table_count(db_session, DbChoice) == 0


def test_list_multiple_choices(db_session: Session) -> None:
    for _ in range(100):
        video_id = insert_bucket_object(db_session).get("id")
        insert_choice(db_session, video_id)

    result = list_choices(db_session)

    assert len(result) == 100
    assert table_count(db_session, DbChoice) == 100


def test_update_choice(db_session: Session) -> None:
    video_id_1 = insert_bucket_object(db_session).get("id")
    choice_id = insert_choice(db_session, video_id_1).get("id")

    video_id_2 = insert_bucket_object(db_session).get("id")
    update_choice(db_session, choice_id, **{"bucket_object_id": video_id_2})

    result = db_session.get(DbChoice, choice_id)
    assert result.bucket_object_id == video_id_2
    assert table_count(db_session, DbChoice) == 1


def test_delete_choice(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    choice_id = insert_choice(db_session, video_id).get("id")

    delete_choice(db_session, choice_id)

    result = db_session.get(DbChoice, choice_id)
    assert result is None
    assert table_count(db_session, DbChoice) == 0


def test_delete_one_of_two_choices(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    choice_id = insert_choice(db_session, video_id).get("id")
    insert_choice(db_session, video_id).get("id")

    delete_choice(db_session, choice_id)

    result = db_session.get(DbChoice, choice_id)
    assert result is None
    assert table_count(db_session, DbChoice) == 1
