from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.core.models.submission import Submission
from app.database.tables.submissions import DbSubmission
from app.repositories.submissions import (
    add_submission, delete_submission, get_submission, list_submissions, update_submission
)
from tests.database.data_inserts import (
    insert_assessment, insert_bucket_object, insert_exercise, insert_multiple_choice,
    insert_submission
)
from tests.database.utils import table_count


def test_add_submission(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    multiple_choice_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, multiple_choice_id).get("id")
    assessment_id = insert_assessment(db_session).get("id")
    submission = Submission(
        user_name=str(uuid4()),
        assessment_id=assessment_id,
        exercise_id=exercise_id,
        multiple_choice_id=multiple_choice_id,
        answer=MultipleChoiceAnswer(choices=[uuid4(), uuid4(), uuid4()])
    )

    add_submission(db_session, submission)

    db_submission = db_session.get(DbSubmission, submission.id)
    assert db_submission.id == submission.id
    assert db_submission.user_name == submission.user_name
    assert db_submission.assessment_id == submission.assessment_id
    assert db_submission.exercise_id == submission.exercise_id
    assert db_submission.multiple_choice_id == submission.multiple_choice_id
    assert db_submission.choices == submission.answer.choices
    assert table_count(db_session, DbSubmission) == 1


def test_get_submission_by_id(db_session: Session) -> None:
    choice_uuid = uuid4()
    video_id = insert_bucket_object(db_session).get("id")
    multiple_choice_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, multiple_choice_id).get("id")
    submission_id = insert_submission(
        db_session,
        exercise_id,
        multiple_choice_id,
        choices=[choice_uuid],
    ).get("id")

    result = get_submission(db_session, submission_id)

    assert result.id == submission_id
    assert result.answer.choices == [choice_uuid]
    assert table_count(db_session, DbSubmission) == 1


def test_list_no_submissions(db_session: Session) -> None:
    result = list_submissions(db_session)
    assert result == []


def test_list_multiple_submissions(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    multiple_choice_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, multiple_choice_id).get("id")
    for i in range(100):
        insert_submission(db_session, exercise_id, multiple_choice_id, choices=[])

    result = list_submissions(db_session)

    assert len(result) == 100
    assert table_count(db_session, DbSubmission) == 100


def test_update_submission(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    multiple_choice_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, multiple_choice_id).get("id")
    submission_id = insert_submission(
        db_session,
        exercise_id,
        multiple_choice_id,
        choices=[uuid4()],
    ).get("id")

    new_choices = [uuid4()]
    update_submission(db_session, submission_id, **{"choices": new_choices})

    result = db_session.get(DbSubmission, submission_id)
    assert result.choices == new_choices
    assert table_count(db_session, DbSubmission) == 1


def test_delete_submission(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    multiple_choice_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, multiple_choice_id).get("id")
    submission_id = insert_submission(
        db_session,
        exercise_id,
        multiple_choice_id,
        choices=[uuid4()],
    ).get("id")

    delete_submission(db_session, submission_id)

    result = db_session.get(DbSubmission, submission_id)
    assert result is None
    assert table_count(db_session, DbSubmission) == 0


def test_delete_one_of_two_submissions(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    multiple_choice_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, multiple_choice_id).get("id")
    submission_id = insert_submission(
        db_session,
        exercise_id,
        multiple_choice_id,
        choices=[uuid4()],
    ).get("id")
    insert_submission(db_session, exercise_id, multiple_choice_id, choices=[])

    delete_submission(db_session, submission_id)

    result = db_session.get(DbSubmission, submission_id)
    assert result is None
    assert table_count(db_session, DbSubmission) == 1
