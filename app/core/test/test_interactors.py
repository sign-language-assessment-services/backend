from app.core.interactors.assessments import (
    get_assessment_by_id, score_assessment
)
from app.core.models.assessment import Assessment
from app.core.models.choice import Choice
from app.core.models.multiple_choice import MultipleChoice

from unittest.mock import Mock


assessment_mock = Mock()
assessment_mock.score = Mock(return_value=42)

repository_mock = Mock()
repository_mock.get = Mock(return_value=assessment_mock)


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


def test_score_assessment_returns_correct_data_structure():
    assessment_id = 1
    submission = {0: [1], 1: [0, 2]}
    result = score_assessment(assessment_id, submission)
    assert isinstance(result, dict)
    assert "score" in result
    assert isinstance(result["score"], int)


def test_assessment_by_id():
    assessment_id = 1
    assessment = get_assessment_by_id(assessment_id)
    assert isinstance(assessment, Assessment)
    assert assessment.name == "Elefantenprüfung"


def test_score_assessment_returns_correct_score():
    assessment_id = 1
    submission = {0: [1], 1: [0, 2]}
    result = score_assessment(assessment_id, submission)
    assert result == {"score": 3}
