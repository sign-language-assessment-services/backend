from unittest.mock import Mock, patch

from app.services.submission_service import SubmissionService
from tests.data.models.assessments import assessment_1
from tests.data.models.submissions import (
    submission_1, submission_2, submission_3, submission_4, submission_5, submission_6
)
from tests.data.models.users import test_taker_1


@patch("app.services.submission_service.add_submission")
def test_add_subission(mocked_add_submission, submission_service: SubmissionService) -> None:
    mocked_session = Mock()

    submission_service.add_submission(mocked_session, submission_1)

    mocked_add_submission.assert_called_once_with(session=mocked_session, submission=submission_1)


@patch(
    "app.services.submission_service.get_submission",
    return_value=submission_1
)
def test_get_submission_by_id(mocked_get_submission, submission_service: SubmissionService) -> None:
    submission_id = mocked_get_submission.return_value.id
    mocked_session = Mock()

    submission = submission_service.get_submission_by_id(mocked_session, submission_id)

    assert submission == mocked_get_submission.return_value
    mocked_get_submission.assert_called_once_with(session=mocked_session, _id=submission_id)


@patch(
    "app.services.submission_service.list_submissions",
    return_value=[submission_1, submission_2, submission_3, submission_4, submission_5, submission_6]
)
def test_list_submissions(mocked_list_submission, submission_service: SubmissionService) -> None:
    mocked_session = Mock()

    submissions = submission_service.list_submissions(mocked_session)

    assert len(submissions) == len(mocked_list_submission.return_value)
    for result, expected in zip(submissions, mocked_list_submission.return_value):
        assert result == expected
    mocked_list_submission.assert_called_once_with(session=mocked_session)


@patch(
    "app.services.submission_service.list_assessment_submissions_for_user",
    return_value=[submission_1, submission_2]
)
def test_get_all_submissions_for_assessment_and_user(
        mocked_list_submission,
        submission_service: SubmissionService
) -> None:
    mocked_session = Mock()
    user_id = test_taker_1.id
    assessment_id = assessment_1.id

    submissions = submission_service.get_all_submissions_for_assessment_and_user(
        mocked_session,
        user_id,
        assessment_id
    )

    assert len(submissions) == len(mocked_list_submission.return_value)
    mocked_list_submission.assert_called_once_with(
        session=mocked_session,
        user_id=user_id,
        assessment_id=assessment_id
    )
