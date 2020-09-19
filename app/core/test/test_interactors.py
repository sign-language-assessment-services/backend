from unittest.mock import Mock, patch

from app.core.interactors.assessments import (
    get_assessment_by_id, score_assessment
)
from app.core.models.assessment import Assessment
from app.core.models.choice import Choice
from app.core.models.multiple_choice import MultipleChoice


@patch("app.core.interactors.assessments.repository")
def test_assessment_by_id(repository_mock):
    repository_mock.get.return_value = Assessment(
        name="foo",
        items=(
            MultipleChoice(
                description="bar",
                choices=(
                    Choice(label="choice 1", is_correct=False),
                    Choice(label="choice 2", is_correct=True),
                )
            ),
        ),
    )
    assessment_id = 1

    result = get_assessment_by_id(assessment_id)

    repository_mock.get.assert_called_once_with(assessment_id)
    assert result == {
        "items": (
            {
                "choices": (
                    {"is_correct": False, "label": "choice 1"},
                    {"is_correct": True, "label": "choice 2"},
                ),
                "description": "bar"
            },
        ),
        "name": "foo"
    }


@patch("app.core.interactors.assessments.repository")
def test_score_assessment_returns_correct_score(repository_mock):
    assessment_mock = mocked_assessment_with_score(42)
    repository_mock.get.return_value = assessment_mock
    assessment_id = 1
    submission = {0: [1], 1: [0, 2]}

    result = score_assessment(assessment_id, submission)

    repository_mock.get.assert_called_once_with(assessment_id)
    assessment_mock.score.assert_called_once_with(submission)
    assert result == {"score": 42}


def mocked_assessment_with_score(score: int):
    assessment_mock = Mock()
    assessment_mock.score.return_value = {"score": score}
    return assessment_mock
