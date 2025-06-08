from unittest.mock import MagicMock, Mock, patch

from app.services import exercise_submission_service as exercise_submission_service_module
from app.services.exercise_submission_service import (
    ExerciseSubmissionService, add_exercise_submission, get_exercise_submission,
    list_exercise_submissions, upsert_exercise_submission
)
from tests.data.models.exercise_submissions import (
    exercise_submission_1, exercise_submission_2, exercise_submission_3, exercise_submission_4,
    exercise_submission_5, exercise_submission_6
)


@patch.object(exercise_submission_service_module, add_exercise_submission.__name__)
def test_add_subission(
        mocked_add_submission: MagicMock,
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    mocked_session = Mock()

    exercise_submission_service.add_submission(mocked_session, exercise_submission_1)

    mocked_add_submission.assert_called_once_with(session=mocked_session, submission=exercise_submission_1)


@patch.object(
    exercise_submission_service_module, get_exercise_submission.__name__,
    return_value=exercise_submission_1
)
def test_get_submission_by_id(
        mocked_get_submission: MagicMock,
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    submission_id = mocked_get_submission.return_value.id
    mocked_session = Mock()

    submission = exercise_submission_service.get_submission_by_id(mocked_session, submission_id)

    assert submission == mocked_get_submission.return_value
    mocked_get_submission.assert_called_once_with(session=mocked_session, _id=submission_id)


@patch.object(
    exercise_submission_service_module, list_exercise_submissions.__name__,
    return_value=[
        exercise_submission_1, exercise_submission_2, exercise_submission_3,
        exercise_submission_4, exercise_submission_5, exercise_submission_6
    ]
)
def test_list_submissions(
        mocked_list_submission: MagicMock,
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    mocked_session = Mock()

    submissions = exercise_submission_service.list_submissions(mocked_session)

    assert len(submissions) == len(mocked_list_submission.return_value)
    for result, expected in zip(submissions, mocked_list_submission.return_value):
        assert result == expected
    mocked_list_submission.assert_called_once_with(session=mocked_session)


@patch.object(exercise_submission_service_module, upsert_exercise_submission.__name__)
def test_upsert_submission(
        mocked_upsert_submission: MagicMock,
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    mocked_session = Mock()

    exercise_submission_service.upsert_submission(mocked_session, exercise_submission_1)

    mocked_upsert_submission.assert_called_once_with(session=mocked_session, submission=exercise_submission_1)
