from uuid import uuid4

from data.models.exercise_submissions import exercise_submission_1, exercise_submission_2
from data.models.exercises import exercise_1

from app.services.scoring_service import ScoringService


def test_correct_single_multiple_choice_answer_scores_exercise_points() -> None:
    scoring_service = ScoringService()
    exercise_score_before = exercise_submission_1.score

    scoring_service.score(exercise_submission_1, exercise_1)
    exercise_score_after = exercise_submission_1.score

    assert exercise_score_before is None
    assert exercise_score_after == exercise_1.points


def test_correct_multiple_multiple_choice_answers_scores_exercise_points() -> None:
    scoring_service = ScoringService()
    exercise_score_before = exercise_submission_1.score
    exercise_1.question_type.content.choices[1].is_correct = True
    exercise_submission_1.answer.choices += [exercise_1.question_type.content.choices[1].id]

    scoring_service.score(exercise_submission_1, exercise_1)
    exercise_score_after = exercise_submission_1.score

    assert exercise_score_before is None
    assert exercise_score_after == exercise_1.points


def test_incorrect_single_multiple_choice_answer_scores_0() -> None:
    scoring_service = ScoringService()
    exercise_score_before = exercise_submission_2.score

    scoring_service.score(exercise_submission_2, exercise_1)
    exercise_score_after = exercise_submission_2.score

    assert exercise_score_before is None
    assert exercise_score_after == 0


def test_partially_correct_multiple_choice_answer_scores_0() -> None:
    scoring_service = ScoringService()
    exercise_score_before = exercise_submission_1.score
    exercise_submission_1.answer.choices += [uuid4()]

    scoring_service.score(exercise_submission_1, exercise_1)
    exercise_score_after = exercise_submission_1.score

    assert exercise_score_before is None
    assert exercise_score_after == 0
