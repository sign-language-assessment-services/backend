from copy import deepcopy
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest

from app.services import exercise_submission_service as exercise_submission_service_module
from app.services.exceptions.not_found import ExerciseSubmissionNotFoundException
from app.services.exercise_submission_service import (
    ExerciseSubmissionService, add_exercise_submission, get_exercise_submission,
    list_exercise_submissions, upsert_exercise_submission
)
from tests.data.models.exercise_submissions import (
    exercise_submission_1, exercise_submission_2, exercise_submission_3, exercise_submission_4,
    exercise_submission_5, exercise_submission_6
)
from tests.data.models.exercises import exercise_1


def test_create_exercise_submission_calls_scoring_function(
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    mocked_session = Mock()
    exercise_submission_service.exercise_service.get_exercise_by_id = Mock(return_value=exercise_1)
    mocked_scoring_function = Mock()
    exercise_submission_service.scoring_service.score = mocked_scoring_function

    exercise_submission_service.create_exercise_submission(
        session=mocked_session,
        assessment_submission_id=exercise_submission_1.assessment_submission_id,
        exercise_id=exercise_submission_1.exercise_id,
        answer_ids=exercise_submission_1.answer.choices
    )

    mocked_scoring_function.assert_called_once()
    assert mocked_scoring_function.call_args.kwargs["exercise"] == exercise_1
    assert mocked_scoring_function.call_args.kwargs["exercise_submission"].answer == exercise_submission_1.answer
    assert mocked_scoring_function.call_args.kwargs["exercise_submission"].score == exercise_submission_1.score


@patch.object(exercise_submission_service_module, add_exercise_submission.__name__)
def test_create_exercise_submission(
        mocked_add_submission: MagicMock,
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    mocked_session = Mock()
    mocked_scoring_function = Mock()
    mocked_get_exercise = Mock(return_value=exercise_1)
    exercise_submission_service.scoring_service.score = mocked_scoring_function
    exercise_submission_service.exercise_service.get_exercise_by_id = mocked_get_exercise

    exercise_submission_service.create_exercise_submission(
        session=mocked_session,
        assessment_submission_id=exercise_submission_1.assessment_submission_id,
        exercise_id=exercise_submission_1.exercise_id,
        answer_ids=exercise_submission_1.answer.choices
    )

    mocked_add_submission.assert_called_once()
    assert mocked_add_submission.call_args.kwargs["session"] == mocked_session
    submission_call = mocked_add_submission.call_args.kwargs["submission"]
    assert submission_call.answer == exercise_submission_1.answer
    assert submission_call.exercise_id == exercise_submission_1.exercise_id
    assert submission_call.assessment_submission_id == exercise_submission_1.assessment_submission_id


@patch.object(
    exercise_submission_service_module, get_exercise_submission.__name__,
    return_value=exercise_submission_1
)
def test_get_exercise_submission_by_id(
        mocked_get_submission: MagicMock,
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    submission_id = mocked_get_submission.return_value.id
    mocked_session = Mock()

    submission = exercise_submission_service.get_exercise_submission_by_id(mocked_session, submission_id)

    assert submission == mocked_get_submission.return_value
    mocked_get_submission.assert_called_once_with(session=mocked_session, _id=submission_id)


@patch.object(
    exercise_submission_service_module, get_exercise_submission.__name__,
    return_value=None
)
def test_get_non_existing_exercise_submission_by_id(
        mocked_get_exercise_submission: MagicMock,
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    mocked_session = Mock()
    non_existing_id = uuid4()

    with pytest.raises(ExerciseSubmissionNotFoundException):
        exercise_submission_service.get_exercise_submission_by_id(mocked_session, non_existing_id)

    mocked_get_exercise_submission.assert_called_once_with(session=mocked_session, _id=non_existing_id)


@patch.object(
    exercise_submission_service_module, list_exercise_submissions.__name__,
    return_value=[
        exercise_submission_1, exercise_submission_2, exercise_submission_3,
        exercise_submission_4, exercise_submission_5, exercise_submission_6
    ]
)
def test_list_exercise_submissions(
        mocked_list_submission: MagicMock,
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    mocked_session = Mock()

    submissions = exercise_submission_service.list_exercise_submissions(mocked_session)

    assert len(submissions) == len(mocked_list_submission.return_value)
    for result, expected in zip(submissions, mocked_list_submission.return_value):
        assert result == expected
    mocked_list_submission.assert_called_once_with(
        session=mocked_session,
        assessment_submission_id=None,
        exercise_id=None
    )


@patch.object(exercise_submission_service_module, upsert_exercise_submission.__name__)
def test_upsert_exercise_submission(
        mocked_upsert_submission: MagicMock,
        exercise_submission_service: ExerciseSubmissionService
) -> None:
    mocked_session = Mock()
    mocked_scoring_function = Mock()
    exercise_submission_service.scoring_service.score = mocked_scoring_function
    exercise_submission_service.exercise_service.get_exercise_by_id = Mock(return_value=exercise_1)

    data=deepcopy(exercise_submission_1.__dict__)
    data["answer"] = [str(choice) for choice in data["answer"].choices]
    assessment_submission_id = data.pop("assessment_submission_id")
    exercise_id = data.pop("exercise_id")

    exercise_submission_service.upsert_exercise_submission(
        session=mocked_session,
        data=data,
        assessment_submission_id=assessment_submission_id,
        exercise_id=exercise_id
    )

    called_submission = mocked_upsert_submission.call_args.kwargs["submission"]
    assert called_submission.assessment_submission_id == assessment_submission_id
    assert called_submission.exercise_id == exercise_id
    assert called_submission.answer == exercise_submission_1.answer
    mocked_scoring_function.assert_called_once_with(
        exercise_submission=exercise_submission_1,
        exercise=exercise_1
    )
