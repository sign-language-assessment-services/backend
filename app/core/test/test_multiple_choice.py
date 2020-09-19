import pytest

from app.core.models.choice import Choice
from app.core.models.multiple_choice import MultipleChoice


@pytest.fixture(name="mocked_multiple_choice")
def multiple_choice():
    return MultipleChoice(
        description="bar",
        choices=(
            Choice(label="foo", is_correct=False),
            Choice(label="foo", is_correct=True),
        )
    )


def test_true_negative_and_false_negative(mocked_multiple_choice):
    assert mocked_multiple_choice.score([]) == 0


def test_true_negative_and_true_positive(mocked_multiple_choice):
    assert mocked_multiple_choice.score([1]) == 1


def test_false_positive_and_false_negative(mocked_multiple_choice):
    assert mocked_multiple_choice.score([0]) == 0


def test_false_positive_true_positive(mocked_multiple_choice):
    assert mocked_multiple_choice.score([0, 1]) == 0


def test_wrong_parameters(mocked_multiple_choice):
    with pytest.raises(ValueError):
        mocked_multiple_choice.score([-42])
    with pytest.raises(ValueError):
        mocked_multiple_choice.score([42])
