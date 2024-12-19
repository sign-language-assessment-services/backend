from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.exercises import DbExercise
from app.database.tables.tasks import DbTask
from tests.database.data_inserts import insert_bucket_object, insert_exercise, insert_multiple_choice


def test_insert_exercise(db_session: Session) -> None:
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )

    data_query = db_session.query(DbExercise)

    assert data_query.count() == 1
    db_exercise = data_query.first()
    assert db_exercise.id == exercise_data.get("id")
    assert db_exercise.bucket_object_id == exercise_data.get("bucket_object_id")


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
    bucket_object_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    multiple_choice_uuid = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{multiple_choice_uuid}\) is not present in table "multiple_choices"'):
        insert_exercise(
            session=db_session,
            bucket_object_id=bucket_object_data.get("id"),
            multiple_choice_id=multiple_choice_uuid
        )


def test_update_exercise(db_session: Session) -> None:
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO, key_suffix="1")
    multiple_choice_data_1 = insert_multiple_choice(session=db_session)
    exercise_data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data_1.get("id")
    )

    multiple_choice_data_2 = insert_multiple_choice(session=db_session)
    db_session.query(DbExercise).update({"multiple_choice_id": multiple_choice_data_2.get("id")})

    data_query = db_session.query(DbExercise)
    assert data_query.count() == 1
    db_exercise = data_query.first()
    assert db_exercise.id == exercise_data.get("id")
    assert db_exercise.multiple_choice_id != multiple_choice_data_1.get("id")
    assert db_exercise.multiple_choice_id == multiple_choice_data_2.get("id")


def test_delete_exercise(db_session):
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    multiple_choice_data = insert_multiple_choice(session=db_session)
    insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )

    db_exercise = db_session.scalar(select(DbExercise))
    db_session.delete(db_exercise)

    assert db_session.query(DbExercise).count() == 0
    assert db_session.query(DbTask).count() == 0
    assert db_session.query(DbBucketObjects).count() == 1
