import pytest

from app.core.models.assessment import Assessment
from app.core.models.choice import Choice
from app.core.models.multiple_choice import MultipleChoice


@pytest.fixture()
def assessment():
    return Assessment(
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


def test_perfect_score(assessment):
    assert assessment.score({0: [1], 1: [0, 2]}) == 2


def test_fifty_percent(assessment):
    assert assessment.score({0: [1], 1: [0, 1]}) == 1


def test_total_failure(assessment):
    assert assessment.score({0: [0], 1: [1]}) == 0
