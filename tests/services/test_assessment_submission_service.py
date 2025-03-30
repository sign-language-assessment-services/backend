from unittest.mock import Mock, patch

from app.services import assessment_submission_service as assessment_submission_service_module
from app.services.assessment_submission_service import (
    AssessmentSubmissionService, add_assessment_submission, get_assessment_submission,
    list_assessment_submissions
)
from tests.data.models.assessment_submissions import (
    assessment_submission_1, assessment_submission_2
)


@patch.object(assessment_submission_service_module, add_assessment_submission.__name__)
def test_add_subission(mocked_add_submission, assessment_submission_service: AssessmentSubmissionService) -> None:
    mocked_session = Mock()

    assessment_submission_service.add_submission(mocked_session, assessment_submission_1)

    mocked_add_submission.assert_called_once_with(session=mocked_session, submission=assessment_submission_1)


@patch.object(
    assessment_submission_service_module, get_assessment_submission.__name__,
    return_value=assessment_submission_1
)
def test_get_submission_by_id(mocked_get_submission, assessment_submission_service: AssessmentSubmissionService) -> None:
    submission_id = mocked_get_submission.return_value.id
    mocked_session = Mock()

    submission = assessment_submission_service.get_submission_by_id(mocked_session, submission_id)

    assert submission == mocked_get_submission.return_value
    mocked_get_submission.assert_called_once_with(session=mocked_session, _id=submission_id)


@patch.object(
    assessment_submission_service_module, list_assessment_submissions.__name__,
    return_value=[assessment_submission_1, assessment_submission_2]
)
def test_list_submissions(mocked_list_submission, assessment_submission_service: AssessmentSubmissionService) -> None:
    mocked_session = Mock()

    submissions = assessment_submission_service.list_submissions(mocked_session)

    assert len(submissions) == len(mocked_list_submission.return_value)
    for result, expected in zip(submissions, mocked_list_submission.return_value):
        assert result == expected
    mocked_list_submission.assert_called_once_with(session=mocked_session)
