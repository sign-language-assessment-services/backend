import pytest

from app.core.models.assessment import Assessment
from app.core.models.exceptions import UnexpectedItemType
from app.core.models.score import Score


def test_perfect_score(assessment: Assessment) -> None:
    assert assessment.score({0: [1], 2: [0]}) == Score(points=2, maximum_points=2)


def test_fifty_percent(assessment: Assessment) -> None:
    assert assessment.score({0: [1], 2: [1]}) == Score(points=1, maximum_points=2)


def test_total_failure(assessment: Assessment) -> None:
    assert assessment.score({0: [0], 2: [1]}) == Score(points=0, maximum_points=2)


def test_score_raises_error_for_static_item(assessment: Assessment) -> None:
    with pytest.raises(UnexpectedItemType):
        assessment.score({1: [0]})
