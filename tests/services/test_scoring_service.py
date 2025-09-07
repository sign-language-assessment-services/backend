from copy import deepcopy
from uuid import uuid4

from app.services.scoring_service import ScoringService
from tests.data.models.exercise_submissions import exercise_submission_1, exercise_submission_2
from tests.data.models.exercises import exercise_1


def test_correct_single_multiple_choice_answer_scores_exercise_points() -> None:
    scoring_service = ScoringService()
    exercise_submission_under_test = deepcopy(exercise_submission_1)
    submission_score_before = exercise_submission_under_test.score

    scoring_service.score(exercise_submission_under_test, exercise_1)
    submission_score_after = exercise_submission_under_test.score

    assert submission_score_before is None
    assert submission_score_after == exercise_1.points


def test_correct_multiple_multiple_choice_answers_scores_exercise_points() -> None:
    scoring_service = ScoringService()
    exercise_under_test = deepcopy(exercise_1)
    exercise_submission_under_test = deepcopy(exercise_submission_1)
    exercise_under_test.question_type.content.choices[1].is_correct = True
    exercise_submission_under_test.answer.choices += [
        exercise_under_test.question_type.content.choices[1].id
    ]
    submission_score_before = exercise_submission_under_test.score

    scoring_service.score(exercise_submission_under_test, exercise_under_test)
    submission_score_after = exercise_submission_under_test.score

    assert submission_score_before is None
    assert submission_score_after == exercise_under_test.points


def test_incorrect_single_multiple_choice_answer_scores_0() -> None:
    scoring_service = ScoringService()
    exercise_submission_under_test = deepcopy(exercise_submission_2)
    submission_score_before = exercise_submission_under_test.score

    scoring_service.score(exercise_submission_under_test, exercise_1)
    submission_score_after = exercise_submission_under_test.score

    assert submission_score_before is None
    assert submission_score_after == 0


def test_partially_correct_multiple_choice_answer_scores_0() -> None:
    scoring_service = ScoringService()
    exercise_submission_under_test = deepcopy(exercise_submission_1)
    exercise_submission_under_test.answer.choices += [uuid4()]
    submission_score_before = exercise_submission_under_test.score

    scoring_service.score(exercise_submission_under_test, exercise_1)
    submission_score_after = exercise_submission_under_test.score

    assert submission_score_before is None
    assert submission_score_after == 0
