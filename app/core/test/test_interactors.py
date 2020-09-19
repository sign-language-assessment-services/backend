import pytest

from app.core.interactors.assessments import (
    get_assessment_by_id, score_assessment
)
from app.core.models.assessment import Assessment
from app.core.models.choice import Choice
from app.core.models.multiple_choice import MultipleChoice

from unittest.mock import Mock, patch

assessment_1 = Assessment(
    name="Elefantenprüfung",
    items=(
        MultipleChoice(
            description="Was essen Elefanten?",
            choices=(
                Choice(
                    label="Spaghetti Bolognese",
                    is_correct=False
                ),
                Choice(
                    label="Nüsse",
                    is_correct=True
                ),
                Choice(
                    label="Menschen",
                    is_correct=False
                )
            )
        ),
        MultipleChoice(
            description="Was trinken Elefanten?",
            choices=(
                Choice(
                    label="Mineralwasser",
                    is_correct=True
                ),
                Choice(
                    label="Limonade",
                    is_correct=False
                ),
                Choice(
                    label="Wasser",
                    is_correct=True
                ),
                Choice(
                    label="Hühnersuppe",
                    is_correct=False
                )
            )
        ),
    )
)

assessment_2 = Assessment(
    name="foo",
    items=(
        MultipleChoice(
            description="bar",
            choices=(
                Choice(label="foo", is_correct=False),
                Choice(label="foo", is_correct=True),
            )
        ),
        MultipleChoice(
            description="bar",
            choices=(
                Choice(label="foo", is_correct=True),
                Choice(label="foo", is_correct=False),
                Choice(label="foo", is_correct=True),
            )
        )
    )
)

repository = {
    1: assessment_1,
    2: assessment_2
}


def test_assessment_by_id():
    assessment_id = 1
    assessment = get_assessment_by_id(assessment_id)
    assert isinstance(assessment, Assessment)
    assert assessment.name == "Elefantenprüfung"


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
