from app.core.models.assessment_result import AssessmentResult, ExerciseScore, SubmissionResult
from tests.data.models.assessment_submissions import (
    assessment_submission_1, assessment_submission_2
)
from tests.data.models.exercises import exercise_1, exercise_2
from tests.data.models.users import test_taker_1

exercise_score_1 = ExerciseScore(
    exercise_id=exercise_1.id,
    score=1,
)
exercise_score_2 = ExerciseScore(
    exercise_id=exercise_2.id,
    score=0,
)

submission_result_1 = SubmissionResult(
    assessment_submission_id=assessment_submission_1.id,
    user_id=test_taker_1.id,
    exercise_scores=[exercise_score_1, exercise_score_2],
    total_score=1,
    finished_at=assessment_submission_1.finished_at
)
submission_result_2 = SubmissionResult(
    assessment_submission_id=assessment_submission_2.id,
    user_id=test_taker_1.id,
    exercise_scores=[exercise_score_1, exercise_score_2],
    total_score=1,
    finished_at=assessment_submission_2.finished_at
)

assessment_result_1 = AssessmentResult(
    submissions=[submission_result_1, submission_result_2]
)
