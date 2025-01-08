from unittest.mock import Mock, patch

from app.services.assessment_service import AssessmentService
from tests.data.models.assessments import assessment_1, assessment_2


@patch(
    "app.services.assessment_service.get_assessment",
    return_value=assessment_1
)
def test_get_assessment_by_id(mocked_get_assessment, assessment_service: AssessmentService) -> None:
    assessment_id = mocked_get_assessment.return_value.id
    mocked_session = Mock()

    assessment = assessment_service.get_assessment_by_id(mocked_session, assessment_id)

    assert assessment.id == assessment_id
    assert assessment.name == mocked_get_assessment.return_value.name
    mocked_get_assessment.assert_called_once_with(session=mocked_session, _id=assessment_id)


@patch(
    "app.services.assessment_service.list_assessments",
    return_value=[assessment_1, assessment_2]
)
def test_list_assessments(mocked_list_assessment, assessment_service: AssessmentService) -> None:
    mocked_session = Mock()

    assessments = assessment_service.list_assessments(mocked_session)

    assert len(assessments) == len(mocked_list_assessment.return_value)
    for result, expected in zip(assessments, mocked_list_assessment.return_value):
        assert result.id == expected.id
        assert result.name == expected.name
    mocked_list_assessment.assert_called_once_with(session=mocked_session)
