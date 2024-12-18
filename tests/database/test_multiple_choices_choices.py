from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.choices import DbChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.multiple_choices_choices import multiple_choices_choices
from database.data_inserts import (
    connect_multiple_choice_with_choices, insert_bucket_object,
    insert_choice, insert_multiple_choice
)


def test_multiple_choice_and_choice_connection(db_session: Session) -> None:
    bucket_1 = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO, suffix="1")
    choice_1 = insert_choice(session=db_session, bucket_object_id=bucket_1.get("id"))
    bucket_2 = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO, suffix="2")
    choice_2 = insert_choice(session=db_session, bucket_object_id=bucket_2.get("id"))
    bucket_3 = insert_bucket_object(session=db_session, content_type=MediaType.IMAGE, suffix="3")
    choice_3 = insert_choice(session=db_session, bucket_object_id=bucket_3.get("id"))
    bucket_4 = insert_bucket_object(session=db_session, content_type=MediaType.IMAGE, suffix="4")
    choice_4 = insert_choice(session=db_session, bucket_object_id=bucket_4.get("id"))
    multiple_choice = insert_multiple_choice(session=db_session)

    connect_multiple_choice_with_choices(
        session=db_session,
        multiple_choice_id=multiple_choice.get("id"),
        choice_ids=[c.get("id") for c in (choice_1, choice_2, choice_3, choice_4)]
    )

    db_multiple_choice = db_session.scalar(db_session.query(DbMultipleChoice))
    association_table_counts = db_session.execute(
        select(func.count()).select_from(multiple_choices_choices)
    ).scalar_one()

    assert len(db_multiple_choice.choices) == 4
    assert association_table_counts == 4


def test_choice_deletion_is_reflected_in_multiple_choice_choices(db_session: Session) -> None:
    multiple_choice = insert_multiple_choice(session=db_session)
    bucket = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    choice_1 = insert_choice(session=db_session, bucket_object_id=bucket.get("id"))
    choice_2 = insert_choice(session=db_session, bucket_object_id=bucket.get("id"))
    choice_3 = insert_choice(session=db_session, bucket_object_id=bucket.get("id"))
    connect_multiple_choice_with_choices(
        session=db_session,
        multiple_choice_id=multiple_choice.get("id"),
        choice_ids=[c.get("id") for c in (choice_1, choice_2, choice_3)]
    )

    db_choice_2 = db_session.scalar(select(DbChoice).where(DbChoice.id == choice_2.get("id")))
    db_session.delete(db_choice_2)
    db_session.flush()
    association_table_counts = db_session.execute(
        select(func.count()).select_from(multiple_choices_choices)
    ).scalar_one()

    assert db_session.query(DbChoice).count() == 2
    assert db_session.query(DbMultipleChoice).count() == 1  # assessment is not deleted
    db_multiple_choice = db_session.scalar(select(DbMultipleChoice))
    assert len(db_multiple_choice.choices) == 2
    assert db_multiple_choice.choices[0].id == choice_1.get("id")
    assert db_multiple_choice.choices[1].id == choice_3.get("id")
    assert association_table_counts == 2


def test_multiple_choice_deletion_does_not_delete_choices(db_session: Session) -> None:
    multiple_choice = insert_multiple_choice(session=db_session)
    bucket = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    choice = insert_choice(session=db_session, bucket_object_id=bucket.get("id"))
    connect_multiple_choice_with_choices(
        session=db_session,
        multiple_choice_id=multiple_choice.get("id"),
        choice_ids=[choice.get("id")]
    )

    db_multiple_choice = db_session.scalar(db_session.query(DbMultipleChoice))
    db_session.delete(db_multiple_choice)
    db_session.flush()
    association_table_counts = db_session.execute(
        select(func.count()).select_from(multiple_choices_choices)
    ).scalar_one()

    assert db_session.query(DbMultipleChoice).count() == 0
    assert db_session.query(DbChoice).count() == 1
    assert association_table_counts == 0
