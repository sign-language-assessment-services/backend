from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.core.models.exercise_submission import ExerciseSubmission
from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.database.exceptions import EntryNotFoundError
from app.database.tables.exercise_submissions import DbExerciseSubmission
from app.repositories.exercise_submissions import (
    add_exercise_submission, delete_exercise_submission, get_exercise_submission,
    get_exercise_submissions_for_assessment_submission, list_exercise_submissions,
    list_exercise_submissions_for_user, update_exercise_submission, upsert_exercise_submission
)
from tests.data.models.users import test_taker_1, test_taker_2
from tests.database.data_inserts import (
    insert_assessment, insert_assessment_submission, insert_bucket_object, insert_exercise,
    insert_exercise_submission, insert_multiple_choice
)
from tests.database.utils import table_count


def test_add_exercise_submission(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    exercise_id = insert_exercise(
        session=db_session,
        bucket_object_id=video_id,
        multiple_choice_id=multiple_choice_id
    ).get("id")
    assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    )

    exercise_submission = ExerciseSubmission(
        assessment_submission_id=assessment_submission.get("id"),
        user_id=assessment_submission.get("user_id"),
        exercise_id=exercise_id,
        answer=MultipleChoiceAnswer(choices=[uuid4(), uuid4(), uuid4()])
    )
    add_exercise_submission(session=db_session, submission=exercise_submission)

    result = db_session.get(DbExerciseSubmission, exercise_submission.id)
    assert result.id == exercise_submission.id
    assert result.created_at == exercise_submission.created_at
    assert result.user_id == exercise_submission.user_id
    assert result.choices == exercise_submission.answer.choices
    assert result.assessment_submission_id == exercise_submission.assessment_submission_id
    assert result.exercise_id == exercise_submission.exercise_id
    assert table_count(db_session, DbExerciseSubmission) == 1


def test_get_exercise_submission_by_id(db_session: Session) -> None:
    choice_uuid = uuid4()
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    exercise_id = insert_exercise(
        session=db_session,
        bucket_object_id=video_id,
        multiple_choice_id=multiple_choice_id
    ).get("id")
    assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    )
    exercise_submission = insert_exercise_submission(
        session=db_session,
        assessment_submission_id=assessment_submission.get("id"),
        exercise_id=exercise_id,
        choices=[choice_uuid],
    )

    result = get_exercise_submission(session=db_session, _id=exercise_submission.get("id"))

    assert result.id == exercise_submission.get("id")
    assert result.created_at == exercise_submission.get("created_at")
    assert result.user_id == exercise_submission.get("user_id")
    assert result.answer.choices == [choice_uuid]
    assert result.assessment_submission_id == exercise_submission.get("assessment_submission_id")
    assert result.exercise_id == exercise_submission.get("exercise_id")
    assert table_count(db_session, DbExerciseSubmission) == 1


def test_get_exercise_submission_by_id_returns_none_if_not_found(db_session: Session) -> None:
    result = get_exercise_submission(session=db_session, _id=uuid4())

    assert result is None


def test_get_exercise_submissions_for_assessment_submission(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    exercise_1_id = insert_exercise(
        session=db_session,
        bucket_object_id=video_id,
        multiple_choice_id=multiple_choice_id
    ).get("id")
    exercise_2_id = insert_exercise(
        session=db_session,
        bucket_object_id=video_id,
        multiple_choice_id=multiple_choice_id
    ).get("id")
    assessment_id = insert_assessment(session=db_session).get("id")
    another_assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission_1_id = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    ).get("id")
    another_assessment_submission_id = insert_assessment_submission(
        session=db_session,
        assessment_id=another_assessment_id
    ).get("id")
    exercise_submission_1 = insert_exercise_submission(
        session=db_session,
        assessment_submission_id=assessment_submission_1_id,
        exercise_id=exercise_1_id,
        choices=[]
    )
    exercise_submission_2 = insert_exercise_submission(
        session=db_session,
        assessment_submission_id=assessment_submission_1_id,
        exercise_id=exercise_2_id,
        choices=[]
    )
    exercise_submission_3 = insert_exercise_submission(
        session=db_session,
        assessment_submission_id=another_assessment_submission_id,
        exercise_id=exercise_2_id,
        choices=[]
    )

    exercise_submissions = get_exercise_submissions_for_assessment_submission(
        session=db_session,
        assessment_submission_id=assessment_submission_1_id
    )

    assert len(exercise_submissions) == 2
    assert exercise_submissions[0].id == exercise_submission_1.get("id")
    assert exercise_submissions[1].id == exercise_submission_2.get("id")
    assert not any(exercise_submission_3.get("id") == s.id for s in exercise_submissions)


def test_list_no_exercise_submissions(db_session: Session) -> None:
    result = list_exercise_submissions(session=db_session)
    assert result == []


def test_list_multiple_exercise_submissions(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission_id = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    ).get("id")
    for i in range(100):
        exercise_id = insert_exercise(
            session=db_session,
            bucket_object_id=video_id,
            multiple_choice_id=multiple_choice_id
        ).get("id")
        insert_exercise_submission(
            session=db_session,
            assessment_submission_id=assessment_submission_id,
            exercise_id=exercise_id,
            choices=[]
        )

    result = list_exercise_submissions(session=db_session)

    assert len(result) == 100
    assert table_count(db_session, DbExerciseSubmission) == 100


def test_update_exercise_submission(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    exercise_id = insert_exercise(
        session=db_session,
        bucket_object_id=video_id,
        multiple_choice_id=multiple_choice_id
    ).get("id")
    assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission_id = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    ).get("id")
    submission = insert_exercise_submission(
        session=db_session,
        assessment_submission_id=assessment_submission_id,
        exercise_id=exercise_id,
        choices=[uuid4()],
    )

    new_choices = [uuid4()]
    update_exercise_submission(
        session=db_session,
        _id=submission.get("id"),
        **{"choices": new_choices}
    )

    result = db_session.get(DbExerciseSubmission, submission.get("id"))
    assert result.id == submission.get("id")
    assert result.created_at == submission.get("created_at")
    assert result.user_id == submission.get("user_id")
    assert result.choices == new_choices
    assert result.assessment_submission_id == submission.get("assessment_submission_id")
    assert result.exercise_id == submission.get("exercise_id")
    assert table_count(db_session, DbExerciseSubmission) == 1


def test_upsert_exercise_submission_with_new_id(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    exercise_id = insert_exercise(
        session=db_session,
        bucket_object_id=video_id,
        multiple_choice_id=multiple_choice_id
    ).get("id")
    assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    )

    exercise_submission = ExerciseSubmission(
        assessment_submission_id=assessment_submission.get("id"),
        user_id=assessment_submission.get("user_id"),
        exercise_id=exercise_id,
        answer=MultipleChoiceAnswer(choices=[uuid4(), uuid4(), uuid4()])
    )
    upsert_exercise_submission(session=db_session, submission=exercise_submission)

    result = db_session.get(DbExerciseSubmission, exercise_submission.id)
    assert result.id == exercise_submission.id
    assert result.created_at == exercise_submission.created_at
    assert result.modified_at is None
    assert result.user_id == exercise_submission.user_id
    assert result.choices == exercise_submission.answer.choices
    assert result.assessment_submission_id == exercise_submission.assessment_submission_id
    assert result.exercise_id == exercise_submission.exercise_id
    assert table_count(db_session, DbExerciseSubmission) == 1


def test_upsert_exercise_submission_with_existing_id(db_session: Session) -> None:
    old_choices = [uuid4()]
    new_choices = [uuid4(), uuid4(), uuid4()]
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    exercise_id = insert_exercise(
        session=db_session,
        bucket_object_id=video_id,
        multiple_choice_id=multiple_choice_id
    ).get("id")
    assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    )
    exercise_submission = insert_exercise_submission(
        session=db_session,
        assessment_submission_id=assessment_submission.get("id"),
        exercise_id=exercise_id,
        choices=old_choices
    )

    updated_exercise_submission = ExerciseSubmission(
        id=exercise_submission.get("id"),
        assessment_submission_id=assessment_submission.get("id"),
        exercise_id=exercise_id,
        user_id=assessment_submission.get("user_id"),
        answer=MultipleChoiceAnswer(choices=new_choices)
    )
    upsert_exercise_submission(session=db_session, submission=updated_exercise_submission)

    result = db_session.get(DbExerciseSubmission, updated_exercise_submission.id)
    assert result.id == exercise_submission.get("id")
    assert result.created_at == exercise_submission.get("created_at")
    assert result.modified_at is not None
    assert result.choices != old_choices and result.choices == new_choices
    assert result.assessment_submission_id == exercise_submission.get("assessment_submission_id")
    assert result.exercise_id == exercise_submission.get("exercise_id")
    assert table_count(db_session, DbExerciseSubmission) == 1


def test_delete_exercise_submission(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    exercise_id = insert_exercise(
        session=db_session,
        bucket_object_id=video_id,
        multiple_choice_id=multiple_choice_id
    ).get("id")
    assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission_id = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    ).get("id")
    submission_id = insert_exercise_submission(
        session=db_session,
        assessment_submission_id=assessment_submission_id,
        exercise_id=exercise_id,
        choices=[uuid4()],
    ).get("id")

    delete_exercise_submission(session=db_session, _id=submission_id)

    result = db_session.get(DbExerciseSubmission, submission_id)
    assert result is None
    assert table_count(db_session, DbExerciseSubmission) == 0


def test_delete_not_existing_exercise_submission_should_fail(db_session: Session) -> None:
    with pytest.raises(EntryNotFoundError, match=r"has no entry with id"):
        delete_exercise_submission(session=db_session, _id=uuid4())


def test_list_exercise_submissions_for_user(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission_id = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    ).get("id")
    user_id_1, user_id_2 = test_taker_1.id, test_taker_2.id
    for i in range(100):
        user_id = user_id_1 if i % 2 else user_id_2
        exercise_id = insert_exercise(
            session=db_session,
            bucket_object_id=video_id,
            multiple_choice_id=multiple_choice_id
        ).get("id")
        insert_exercise_submission(
            session=db_session,
            assessment_submission_id=assessment_submission_id,
            exercise_id=exercise_id,
            choices=[],
            user_id=user_id
        )

    result_1 = list_exercise_submissions_for_user(session=db_session, user_id=user_id_1)
    result_2 = list_exercise_submissions_for_user(session=db_session, user_id=user_id_2)

    assert len(result_1) == 50
    assert len(result_2) == 50
    assert table_count(db_session, DbExerciseSubmission) == 100
