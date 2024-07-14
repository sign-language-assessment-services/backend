from unittest import mock
from unittest.mock import Mock, patch

import pytest

import app.services.assessment_service as assessment_service_module
from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.exceptions import UnexpectedItemType
from app.core.models.score import Score
from app.services.assessment_service import AssessmentService


@patch.object(
    AssessmentService, AssessmentService.get_assessment_by_id.__name__,
    return_value=Assessment(name="Test Assessment", id="1234")
)
def test_get_assessment_by_id(mocked_get_assessment, assessment_service: AssessmentService) -> None:
    assessment_id = "1234"
    mocked_session = Mock()

    assessment = assessment_service.get_assessment_by_id(mocked_session, assessment_id)

    assert assessment.id == assessment_id
    assert assessment.name == "Test Assessment"
    mocked_get_assessment.assert_called_once_with(mocked_session, assessment_id)


@patch.object(
    AssessmentService, AssessmentService.list_assessments.__name__,
    return_value=[
        AssessmentSummary(id="00", name="00"),
        AssessmentSummary(id="01", name="01")
    ]
)
def test_list_assessments(mocked_list_assessment, assessment_service: AssessmentService) -> None:
    mocked_session = Mock()

    assessments = assessment_service.list_assessments(mocked_session)

    assert assessments == [
        AssessmentSummary(id="00", name="00"),
        AssessmentSummary(id="01", name="01")
    ]
    mocked_list_assessment.assert_called_once_with(mocked_session)


# TODO/NOTE: finding the right choice from an answer by giving the position will be replaced by finding it via uuid
@patch.object(assessment_service_module, assessment_service_module.add_submission.__name__)
@patch.object(
    Assessment, Assessment.score.__name__,
    return_value=Score(points=1, maximum_points=1)
)
@patch.object(
    AssessmentService, AssessmentService.get_assessment_by_id.__name__,
    return_value=Assessment(name="Test Assessment", id="foo42")
)
def test_score_assessment(
        mocked_get_assessment, mocked_score, mocked_add_submission, assessment_service: AssessmentService
) -> None:
    answers = [{"item_id": "0", "choice_ids": ["0"]}]
    mocked_session = Mock()

    score = assessment_service.score_assessment(
        assessment_id="foo42",
        answers=answers,
        user_id="001",
        session=mocked_session
    )

    assert score == Score(points=1, maximum_points=1)
    mocked_get_assessment.assert_called_once_with(session=mocked_session, assessment_id="foo42")
    mocked_score.assert_called_once_with(answers=answers)

    called_submission = mocked_add_submission.call_args[1]["submission"]
    assert called_submission.answers == answers
    assert called_submission.assessment_id == "foo42"
    assert called_submission.points == 1
    assert called_submission.maximum_points == 1
    assert called_submission.percentage == 1.0


@patch.object(AssessmentService, AssessmentService.score_assessment.__name__, side_effect=UnexpectedItemType)
def test_score_assessment_raises_exception_on_static_item(_, assessment_service: AssessmentService) -> None:
    with pytest.raises(UnexpectedItemType):
        assessment_service.score_assessment(
            assessment_id="1",
            answers=[{"item_id": 1, "choice_ids": ["1"]}],
            user_id=mock.ANY,
            session=mock.ANY
        )
