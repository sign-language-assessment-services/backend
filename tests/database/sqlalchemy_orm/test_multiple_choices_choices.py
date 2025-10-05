from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.choices import DbChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from tests.database.data_inserts import (
    connect_multiple_choice_with_choices, insert_bucket_object, insert_choice,
    insert_multiple_choice
)
from tests.database.utils import table_count


def test_multiple_choice_and_choice_connection(db_session: Session) -> None:
    bucket_1 = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO, filename="1")
    choice_1 = insert_choice(session=db_session, bucket_object_id=bucket_1.get("id"))
    bucket_2 = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO, filename="2")
    choice_2 = insert_choice(session=db_session, bucket_object_id=bucket_2.get("id"))
    bucket_3 = insert_bucket_object(session=db_session, media_type=MediaType.IMAGE, filename="3")
    choice_3 = insert_choice(session=db_session, bucket_object_id=bucket_3.get("id"))
    bucket_4 = insert_bucket_object(session=db_session, media_type=MediaType.IMAGE, filename="4")
    choice_4 = insert_choice(session=db_session, bucket_object_id=bucket_4.get("id"))
    multiple_choice = insert_multiple_choice(session=db_session)

    connect_multiple_choice_with_choices(
        session=db_session,
        multiple_choice_id=multiple_choice.get("id"),
        choice_ids=[c.get("id") for c in (choice_1, choice_2, choice_3, choice_4)]
    )

    db_multiple_choice = db_session.execute(select(DbMultipleChoice)).scalar_one()
    assert len(db_multiple_choice.choices) == 4
    assert table_count(db_session, DbMultipleChoicesChoices) == 4


def test_choice_deletion_is_reflected_in_asscociation_table(db_session: Session) -> None:
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    bucket = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO)
    choice_1 = insert_choice(session=db_session, bucket_object_id=bucket.get("id"))
    choice_2 = insert_choice(session=db_session, bucket_object_id=bucket.get("id"))
    choice_3 = insert_choice(session=db_session, bucket_object_id=bucket.get("id"))
    connect_multiple_choice_with_choices(
        session=db_session,
        multiple_choice_id=multiple_choice_id,
        choice_ids=[c.get("id") for c in (choice_1, choice_2, choice_3)]
    )

    db_choice_2 = db_session.get(DbChoice, choice_2.get("id"))
    db_session.delete(db_choice_2)

    db_multiple_choice = db_session.get(DbMultipleChoice, multiple_choice_id)
    assert len(db_multiple_choice.choices) == 2
    assert db_multiple_choice.choices[0].id == choice_1.get("id")
    assert db_multiple_choice.choices[1].id == choice_3.get("id")
    assert table_count(db_session, DbChoice) == 2
    assert table_count(db_session, DbMultipleChoicesChoices) == 2
    assert table_count(db_session, DbMultipleChoice) == 1
