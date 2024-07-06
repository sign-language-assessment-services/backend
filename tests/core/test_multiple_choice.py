import pytest

from app.core.models.multiple_choice import MultipleChoice


def test_true_negative_and_false_negative(multiple_choice_question1: MultipleChoice) -> None:
    assert multiple_choice_question1.score({}) == 0


def test_true_negative_and_true_positive(multiple_choice_question1: MultipleChoice) -> None:
    assert multiple_choice_question1.score({"choice_ids": ["1"]}) == 1


def test_false_positive_and_false_negative(multiple_choice_question1: MultipleChoice) -> None:
    assert multiple_choice_question1.score({"choice_ids": ["0"]}) == 0


def test_false_positive_true_positive(multiple_choice_question1: MultipleChoice) -> None:
    assert multiple_choice_question1.score({"choice_ids": ["0", "1"]}) == 0


def test_wrong_parameters(multiple_choice_question1: MultipleChoice) -> None:
    with pytest.raises(ValueError):
        multiple_choice_question1.score({"choice_ids": ["-42"]})
    with pytest.raises(ValueError):
        multiple_choice_question1.score({"choice_ids": ["42"]})
