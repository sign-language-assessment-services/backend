import pytest

from app.core.exceptions import UnexpectedItemType
from app.core.models.assessment import Assessment
from app.core.models.score import Score


@pytest.mark.skip(reason="Scoring has to be re-implemented.")
def test_perfect_score(assessment: Assessment) -> None:
    answer = [{"item_id": "0", "choice_ids": ["1"]}, {"item_id": "2", "choice_ids": ["0"]}]
    assert assessment.score(answer) == Score(points=2, maximum_points=2)


@pytest.mark.skip(reason="Scoring has to be re-implemented.")
def test_fifty_percent(assessment: Assessment) -> None:
    answer = [{"item_id": "0", "choice_ids": ["1"]}, {"item_id": "2", "choice_ids": ["1"]}]
    assert assessment.score(answer) == Score(points=1, maximum_points=2)


@pytest.mark.skip(reason="Scoring has to be re-implemented.")
def test_total_failure(assessment: Assessment) -> None:
    answer = [{"item_id": "0", "choice_ids": ["0"]}, {"item_id": "2", "choice_ids": ["1"]}]
    assert assessment.score(answer) == Score(points=0, maximum_points=2)


@pytest.mark.skip(reason="Scoring has to be re-implemented.")
def test_score_raises_error_for_static_item(assessment: Assessment) -> None:
    with pytest.raises(UnexpectedItemType):
        assessment.score([{"item_id": "1", "choice_ids": ["0"]}])
