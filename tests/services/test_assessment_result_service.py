from unittest.mock import MagicMock, Mock, patch

from app.core.models.assessment_result import AssessmentResult, SubmissionResult
from app.services import assessment_result_service as assessment_result_service_module
from app.services.assessment_result_service import (
    AssessmentResultService, list_finished_assessment_submissions_for_assessment
)
from tests.data.models.assessment_submissions import (
    assessment_submission_1, assessment_submission_2
)
from tests.data.models.assessments import assessment_1


@patch.object(
    assessment_result_service_module, list_finished_assessment_submissions_for_assessment.__name__,
    return_value=[assessment_submission_1, assessment_submission_2]
)
def test_get_assessment_result(
        mocked_list_finished_submission: MagicMock,
        assessment_result_service: AssessmentResultService
) -> None:
    mocked_session = Mock()

    assessment_result = assessment_result_service.get_assessment_result(mocked_session, assessment_1.id)

    # TODO: add exercise scores in test data (yet empty)
    assert assessment_result == AssessmentResult(
        submissions=[
            SubmissionResult(
                assessment_submission_id=assessment_submission_1.id,
                user_id=assessment_submission_1.user_id,
                exercise_scores=[],
                total_score=1.0,
                finished_at=assessment_submission_1.finished_at
            ),
            SubmissionResult(
                assessment_submission_id=assessment_submission_2.id,
                user_id=assessment_submission_2.user_id,
                exercise_scores=[],
                total_score=0.0,
                finished_at=assessment_submission_2.finished_at
            )
        ]
    )
    mocked_list_finished_submission.assert_called_once_with(session=mocked_session, assessment_id=assessment_1.id)
