from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.models.media_types import MediaType
from app.database.tables.assessments import DbAssessment
from app.database.tables.bucket_objects import DbBucketObjects
from app.database.tables.exercises import DbExercise
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.primers import DbPrimer
from app.database.tables.submissions import DbSubmission
from database.data_inserts import insert_bucket_object, insert_exercise, insert_multiple_choice, insert_submission


def test_insert_valid_submission(db_session):
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )
    submission_data = insert_submission(
        session=db_session,
        exercise_id=exercise_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )

    data_query = db_session.query(DbSubmission)

    assert data_query.count() == 1
    db_submission = data_query.first()
    assert db_submission.id == submission_data.get("id")
    assert db_submission.created_at == submission_data.get("created_at")
    assert db_submission.user_name == submission_data.get("user_name")
    assert db_submission.choices == submission_data.get("choices")
    assert db_submission.exercise_id == exercise_data.get("id")
    assert db_submission.multiple_choice_id == multiple_choice_data.get("id")


def test_insert_submission_with_missing_exercise_id_fails(db_session):
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_id = uuid4()  # does not exist in database

    with pytest.raises(IntegrityError, match=fr'{exercise_id}.*not present in table "exercises"'):
        insert_submission(
            session=db_session,
            exercise_id=exercise_id,
            multiple_choice_id=multiple_choice_data.get("id")
        )


def test_insert_submission_with_missing_multiple_choice_id_fails(db_session):
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
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
            multiple_choice_id=multiple_choice_id
        )


def test_delete_submissions(db_session):
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_data = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )
    insert_submission(
        session=db_session,
        exercise_id=exercise_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )

    db_submission = db_session.scalar(select(DbSubmission))
    db_session.delete(db_submission)

    assert db_session.query(DbSubmission).count() == 0
    # Deletion of submission should not trigger other deletions
    assert db_session.query(DbBucketObjects).count() == 1
    assert db_session.query(DbMultipleChoice).count() == 1
    assert db_session.query(DbExercise).count() == 1
