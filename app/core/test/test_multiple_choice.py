import pytest

from app.core.models.choice import Choice
from app.core.models.multiple_choice import MultipleChoice


@pytest.fixture()
def multiple_choice():
    return MultipleChoice(
        description="bar",
        choices=(
            Choice(label="foo", is_correct=False),
            Choice(label="foo", is_correct=True),
        )
    )


def test_true_negative_and_false_negative(multiple_choice):
    assert multiple_choice.score([]) == 0


def test_true_negative_and_true_positive(multiple_choice):
    assert multiple_choice.score([1]) == 1


def test_false_positive_and_false_negative(multiple_choice):
    assert multiple_choice.score([0]) == 0


def test_false_positive_true_positive(multiple_choice):
    assert multiple_choice.score([0, 1]) == 0


def test_wrong_parameters(multiple_choice):
    with pytest.raises(ValueError):
        multiple_choice.score([-42])
    with pytest.raises(ValueError):
        multiple_choice.score([42])
