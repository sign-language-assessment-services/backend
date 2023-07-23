from unittest.mock import Mock


def test_perfect_score(mocked_assessment: Mock) -> None:
    assert mocked_assessment.score({0: [1], 1: [0]}) == {"score": 2}


def test_fifty_percent(mocked_assessment: Mock) -> None:
    assert mocked_assessment.score({0: [1], 1: [1]}) == {"score": 1}


def test_total_failure(mocked_assessment: Mock) -> None:
    assert mocked_assessment.score({0: [0], 1: [1]}) == {"score": 0}
