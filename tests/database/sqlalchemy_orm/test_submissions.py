from uuid import uuid4

import pytest
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.exercises import DbExercise
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.submissions import DbSubmission
from tests.database.data_inserts import (
    insert_bucket_object, insert_exercise, insert_multiple_choice, insert_submission
)
from tests.database.utils import table_count


def test_insert_submission(db_session):
    bucket_object_data = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO)
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_object_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )

    submission_data = insert_submission(
        session=db_session,
        exercise_id=exercise_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id"),
        choices=[uuid4()]
    )

    db_submission = db_session.get(DbSubmission, submission_data.get("id"))
    assert table_count(db_session, DbSubmission) == 1
    assert db_submission.id == submission_data.get("id")
    assert db_submission.created_at == submission_data.get("created_at")
    assert db_submission.user_name == submission_data.get("user_name")
    assert db_submission.choices == [choice for choice in submission_data.get("choices")]
    assert db_submission.exercise_id == exercise_data.get("id")
    assert db_submission.multiple_choice_id == multiple_choice_data.get("id")


def test_insert_submission_with_missing_exercise_id_fails(db_session: Session) -> None:
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_id = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{exercise_id}.*not present in table "exercises"'):
        insert_submission(
            session=db_session,
            exercise_id=exercise_id,
            multiple_choice_id=multiple_choice_data.get("id"),
            choices=[uuid4()]
        )


def test_insert_submission_with_missing_multiple_choice_id_fails(db_session: Session) -> None:
    bucket_data = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO)
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )
    multiple_choice_id = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{multiple_choice_id}.*not present in table "multiple_choices"'):
        insert_submission(
            session=db_session,
            exercise_id=exercise_data.get("id"),
            multiple_choice_id=multiple_choice_id,
            choices=[uuid4()]
        )


def test_update_submission(db_session: Session) -> None:
    bucket_object_data = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO)
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_object_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )
    submission_data = insert_submission(
        session=db_session,
        exercise_id=exercise_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id"),
        choices=[uuid4()]
    )

    new_choices = [uuid4(), uuid4()]
    db_session.execute(update(DbSubmission).values(choices=new_choices))

    db_submission = db_session.get(DbSubmission, submission_data.get("id"))
    assert table_count(db_session, DbSubmission) == 1
    assert db_submission.id == submission_data.get("id")
    assert db_submission.choices != [choice for choice in submission_data.get("choices")]
    assert db_submission.choices == [choice for choice in new_choices]


def test_delete_submissions(db_session: Session) -> None:
    bucket_data = insert_bucket_object(session=db_session, media_type=MediaType.VIDEO)
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )
    insert_submission(
        session=db_session,
        exercise_id=exercise_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id"),
        choices=[uuid4()]
    )

    db_submission = db_session.scalar(select(DbSubmission))
    db_session.delete(db_submission)

    assert table_count(db_session, DbSubmission) == 0
    assert table_count(db_session, DbBucketObjects) == 1
    assert table_count(db_session, DbMultipleChoice) == 1
    assert table_count(db_session, DbExercise) == 1
