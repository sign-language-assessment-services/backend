from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.exercises import DbExercise
from app.database.tables.tasks import DbTask
from tests.database.data_inserts import insert_bucket_object, insert_exercise, insert_multiple_choice, insert_task


def test_insert_valid_exercise(db_session: Session) -> None:
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    multiple_choice_data = insert_multiple_choice(session=db_session)
    data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )

    data_query = db_session.query(DbExercise)

    assert data_query.count() == 1
    db_exercise = data_query.first()
    assert db_exercise.id == data.get("id")
    assert db_exercise.bucket_object_id == data.get("bucket_object_id")


def test_insert_exercise_with_non_existing_bucket_object_fails(db_session):
    task_data = insert_task(session=db_session, task_type="exercise")
    multiple_choice_data = insert_multiple_choice(session=db_session)
    bucket_uuid = uuid4()  # does not exist in database
    data = {
        "id": task_data.get("id"),
        "bucket_object_id": bucket_uuid,
        "multiple_choice_id": multiple_choice_data.get("id"),
        "points": 1
    }

    with pytest.raises(IntegrityError, match=fr'{bucket_uuid}\) is not present in table "bucket_objects"'):
        _add_exercise_data(db_session, **data)


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
    assert db_session.query(DbTask).count() == 0  # Task should be deleted as well
    assert db_session.query(DbBucketObjects).count() == 1  # Bucket object should not be deleted


def _add_exercise_data(session, **kwargs) -> None:
    statement = text(
        """
        INSERT INTO exercises(points, id, bucket_object_id, multiple_choice_id)
        VALUES (:points, :id, :bucket_object_id, :multiple_choice_id)
        """
    )
    session.execute(statement, kwargs)


# TODO: From 2024-11-24...
# TODO: complete other tests, here in submissions folder as well as not written ones
# TODO: Why is Task not deleted (Deletion on Exercise and Primer should delete Task as well)
# TODO: Fix app by including new database code
# TODO: Fix app by using new Pydantic models
