import pytest

from app.core.models.assessment import Assessment
from app.core.models.choice import Choice
from app.core.models.multiple_choice import MultipleChoice


@pytest.fixture(name="mocked_assessment")
def assessment():
    return Assessment(
        name="foo",
        items=(
            MultipleChoice(
                description="description 1",
                choices=(
                    Choice(label="choice 1-A", is_correct=False),
                    Choice(label="choice 1-B", is_correct=True),
                )
            ),
            MultipleChoice(
                description="description 2",
                choices=(
                    Choice(label="choice 2-A", is_correct=True),
                    Choice(label="choice 2-B", is_correct=False),
                    Choice(label="choice 2-C", is_correct=True),
                )
            )
        )
    )


def test_perfect_score(mocked_assessment):
    assert mocked_assessment.score({0: [1], 1: [0, 2]}) == {"score": 2}


def test_fifty_percent(mocked_assessment):
    assert mocked_assessment.score({0: [1], 1: [0, 1]}) == {"score": 1}


def test_total_failure(mocked_assessment):
    assert mocked_assessment.score({0: [0], 1: [1]}) == {"score": 0}
