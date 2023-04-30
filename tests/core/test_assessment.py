from unittest.mock import Mock

import pytest

from app.core.models.assessment import Assessment
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.text_choice import TextChoice
from app.core.models.text_question import TextQuestion


@pytest.fixture(name="mocked_assessment")
def assessment() -> Assessment:
    return Assessment(
        name="foo",
        items=(
            MultipleChoice(
                question=TextQuestion(text="question 1"),
                choices=(
                    TextChoice(text="choice 1-A", is_correct=False),
                    TextChoice(text="choice 1-B", is_correct=True),
                )
            ),
            MultipleChoice(
                question=TextQuestion(text="question 2"),
                choices=(
                    TextChoice(text="choice 2-A", is_correct=True),
                    TextChoice(text="choice 2-B", is_correct=False),
                    TextChoice(text="choice 2-C", is_correct=True),
                )
            )
        )
    )


def test_perfect_score(mocked_assessment: Mock) -> None:
    assert mocked_assessment.score({0: [1], 1: [0, 2]}) == {"score": 2}


def test_fifty_percent(mocked_assessment: Mock) -> None:
    assert mocked_assessment.score({0: [1], 1: [0, 1]}) == {"score": 1}


def test_total_failure(mocked_assessment: Mock) -> None:
    assert mocked_assessment.score({0: [0], 1: [1]}) == {"score": 0}
