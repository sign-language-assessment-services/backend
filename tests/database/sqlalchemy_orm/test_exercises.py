from uuid import uuid4

import pytest
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.exercises import DbExercise
from app.database.tables.tasks import DbTask
from database.data_inserts import insert_bucket_object, insert_exercise, insert_multiple_choice
from database.utils import table_count


def test_insert_exercise(db_session: Session) -> None:
    bucket_object_id = insert_bucket_object(db_session).get("id")
    multiple_choice_id = insert_multiple_choice(db_session).get("id")

    exercise_id = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_object_id,
        multiple_choice_id=multiple_choice_id
    ).get("id")

    db_exercise = db_session.get(DbExercise, exercise_id)
    assert db_exercise.id == exercise_id
    assert db_exercise.bucket_object_id == bucket_object_id
    assert table_count(db_session, DbExercise) == 1


def test_insert_exercise_with_non_existing_bucket_object_fails(db_session):
    multiple_choice_data = insert_multiple_choice(session=db_session)
    bucket_uuid = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{bucket_uuid}\) is not present in table "bucket_objects"'):
        insert_exercise(
            session=db_session,
            bucket_object_id=bucket_uuid,
            multiple_choice_id=multiple_choice_data.get("id")
        )


def test_insert_exercise_with_non_existing_multiple_choice_object_fails(db_session):
    bucket_object_data = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO)
    multiple_choice_uuid = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{multiple_choice_uuid}\) is not present in table "multiple_choices"'):
        insert_exercise(
            session=db_session,
            bucket_object_id=bucket_object_data.get("id"),
            multiple_choice_id=multiple_choice_uuid
        )


def test_update_exercise(db_session: Session) -> None:
    bucket_data = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO, filename="1")
    multiple_choice_data_1 = insert_multiple_choice(session=db_session)
    exercise_data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data_1.get("id")
    )

    multiple_choice_data_2 = insert_multiple_choice(session=db_session)
    db_session.execute(update(DbExercise).values(multiple_choice_id=multiple_choice_data_2.get("id")))

    db_exercise = db_session.get(DbExercise, exercise_data.get("id"))
    assert table_count(db_session, DbExercise) == 1
    assert db_exercise.id == exercise_data.get("id")
    assert db_exercise.multiple_choice_id != multiple_choice_data_1.get("id")
    assert db_exercise.multiple_choice_id == multiple_choice_data_2.get("id")


def test_delete_exercise(db_session):
    bucket_data_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data_id,
        multiple_choice_id=multiple_choice_id
    )

    db_exercise = db_session.scalar(select(DbExercise))
    db_session.delete(db_exercise)

    assert table_count(db_session, DbExercise) == 0
    assert table_count(db_session, DbTask) == 0
    assert table_count(db_session, DbBucketObjects) == 1
