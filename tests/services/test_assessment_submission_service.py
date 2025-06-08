from datetime import datetime
from unittest.mock import ANY, MagicMock, Mock, patch

from app.services import assessment_submission_service as assessment_submission_service_module
from app.services.assessment_submission_service import (
    AssessmentSubmissionService, add_assessment_submission, get_assessment_submission,
    get_exercise_submissions_for_assessment_submission, list_assessment_submissions,
    update_assessment_submission
)
from tests.data.models.assessment_submissions import (
    assessment_submission_1, assessment_submission_2
)
from tests.data.models.exercise_submissions import exercise_submission_5, exercise_submission_6


@patch.object(assessment_submission_service_module, add_assessment_submission.__name__)
def test_add_subission(
        mocked_add_submission: MagicMock,
        assessment_submission_service: AssessmentSubmissionService
) -> None:
    mocked_session = Mock()

    assessment_submission_service.add_submission(mocked_session, assessment_submission_1)

    mocked_add_submission.assert_called_once_with(session=mocked_session, submission=assessment_submission_1)


@patch.object(
    assessment_submission_service_module, get_assessment_submission.__name__,
    return_value=assessment_submission_1
)
def test_get_submission_by_id(
        mocked_get_submission: MagicMock,
        assessment_submission_service: AssessmentSubmissionService
) -> None:
    submission_id = mocked_get_submission.return_value.id
    mocked_session = Mock()

    submission = assessment_submission_service.get_submission_by_id(mocked_session, submission_id)

    assert submission == mocked_get_submission.return_value
    mocked_get_submission.assert_called_once_with(session=mocked_session, _id=submission_id)


@patch.object(
    assessment_submission_service_module, list_assessment_submissions.__name__,
    return_value=[assessment_submission_1, assessment_submission_2]
)
def test_list_submissions(
        mocked_list_submission: MagicMock,
        assessment_submission_service: AssessmentSubmissionService
) -> None:
    mocked_session = Mock()

    submissions = assessment_submission_service.list_submissions(mocked_session)

    assert len(submissions) == len(mocked_list_submission.return_value)
    for result, expected in zip(submissions, mocked_list_submission.return_value):
        assert result == expected
    mocked_list_submission.assert_called_once_with(session=mocked_session)


@patch.object(
    assessment_submission_service_module, get_exercise_submissions_for_assessment_submission.__name__,
    return_value=[exercise_submission_5, exercise_submission_6]
)
@patch.object(assessment_submission_service_module, get_assessment_submission.__name__)
@patch.object(assessment_submission_service_module, update_assessment_submission.__name__)
def test_update_submission_finished(update_assessment_submission_mock: MagicMock, *args: MagicMock) -> None:
    mocked_session = Mock()
    assessment_submission_service = AssessmentSubmissionService(mocked_session)

    assessment_submission_service.update_submission(
        session=mocked_session,
        submission_id=assessment_submission_1.id,
        finished=True
    )

    update_assessment_submission_mock.assert_called_once_with(
        mocked_session,
        assessment_submission_1.id,
        finished=True,
        score=1.0,
        finished_at=ANY
    )
    finished_at = update_assessment_submission_mock.call_args.kwargs["finished_at"]
    assert isinstance(finished_at, datetime)
    assert finished_at > assessment_submission_1.created_at
