from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.models.choice import Choice
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.choices import DbChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from app.repositories.multiple_choices import (
    add_multiple_choice, delete_multiple_choice, get_multiple_choice, list_multiple_choices, update_multiple_choice
)
from tests.database.data_inserts import insert_bucket_object, insert_multiple_choice
from tests.database.utils import table_count


def test_add_multiple_choice(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    choice_content = MultimediaFile(
        id=video_id,
        location=MinioLocation(bucket="1", key="test.mpg"),
        media_type=MediaType.VIDEO
    )
    choice_1 = Choice(content=choice_content, is_correct=True)
    choice_2 = Choice(content=choice_content, is_correct=False)
    choice_3 = Choice(content=choice_content, is_correct=False)
    multiple_choice = MultipleChoice(choices=[choice_1, choice_2, choice_3])

    add_multiple_choice(db_session, multiple_choice)

    result = db_session.get(DbMultipleChoice, multiple_choice.id)
    assert result.id == multiple_choice.id
    for index, choice in enumerate([choice_1, choice_2, choice_3]):
        assert result.choices[index].id == choice.id
        assert result.associations[index].choice_id == choice.id
        assert result.associations[index].multiple_choice_id == multiple_choice.id
        assert result.associations[index].position == index + 1
        assert result.associations[index].is_correct is choice.is_correct
    assert table_count(db_session, DbMultipleChoice) == 1
    assert table_count(db_session, DbChoice) == 3
    assert table_count(db_session, DbMultipleChoicesChoices) == 3


def test_get_multiple_choice_by_id(db_session: Session) -> None:
    multiple_choice_id = insert_multiple_choice(db_session).get("id")

    result = get_multiple_choice(db_session, multiple_choice_id)

    assert result.id == multiple_choice_id
    assert table_count(db_session, DbMultipleChoice) == 1


def test_list_no_multiple_choices(db_session: Session) -> None:
    result = list_multiple_choices(db_session)

    assert result == []
    assert table_count(db_session, DbMultipleChoice) == 0


def test_list_multiple_multiple_choices(db_session: Session) -> None:
    for _ in range(100):
        insert_multiple_choice(db_session)

    result = list_multiple_choices(db_session)

    assert len(result) == 100
    assert table_count(db_session, DbMultipleChoice) == 100


def test_update_multiple_choice(db_session: Session) -> None:
    multiple_choice_id = insert_multiple_choice(db_session).get("id")

    updated_time = datetime(2001, 1, 1, 1, tzinfo=UTC)
    update_multiple_choice(db_session, multiple_choice_id, **{"created_at": updated_time})

    result = db_session.get(DbMultipleChoice, multiple_choice_id)
    assert result.created_at == updated_time
    assert table_count(db_session, DbMultipleChoice) == 1


def test_delete_multiple_choice(db_session: Session) -> None:
    multiple_choice_id = insert_multiple_choice(db_session).get("id")

    delete_multiple_choice(db_session, multiple_choice_id)

    result = db_session.get(DbMultipleChoice, multiple_choice_id)
    assert result is None
    assert table_count(db_session, DbMultipleChoice) == 0


def test_delete_one_of_two_multiple_choices(db_session: Session) -> None:
    multiple_choice_id = insert_multiple_choice(db_session).get("id")
    insert_multiple_choice(db_session).get("id")

    delete_multiple_choice(db_session, multiple_choice_id)

    result = db_session.get(DbMultipleChoice, multiple_choice_id)
    assert result is None
    assert table_count(db_session, DbMultipleChoice) == 1
