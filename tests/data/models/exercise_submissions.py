from uuid import uuid4

from app.core.models.exercise_submission import ExerciseSubmission
from tests.data.models.assessment_submissions import assessment_submission_1
from tests.data.models.exercises import exercise_1, exercise_2
from tests.data.models.multiple_choice_answer import (
    multiple_choice_answer_1, multiple_choice_answer_2
)
from tests.data.models.users import test_taker_1, test_taker_2

exercise_submission_1 = ExerciseSubmission(
    id=uuid4(),
    user_id=test_taker_1.id,
    assessment_submission_id=assessment_submission_1.id,
    exercise_id=exercise_1.id,
    answer=multiple_choice_answer_1,
)

exercise_submission_2 = ExerciseSubmission(
    id=uuid4(),
    user_id=test_taker_1.id,
    assessment_submission_id=assessment_submission_1.id,
    exercise_id=exercise_1.id,
    answer=multiple_choice_answer_2,
)

exercise_submission_3 = ExerciseSubmission(
    id=uuid4(),
    user_id=test_taker_1.id,
    assessment_submission_id=assessment_submission_1.id,
    exercise_id=exercise_2.id,
    answer=multiple_choice_answer_1,
)

exercise_submission_4 = ExerciseSubmission(
    id=uuid4(),
    user_id=test_taker_1.id,
    assessment_submission_id=assessment_submission_1.id,
    exercise_id=exercise_2.id,
    answer=multiple_choice_answer_2,
)

exercise_submission_5 = ExerciseSubmission(
    id=uuid4(),
    user_id=test_taker_2.id,
    assessment_submission_id=assessment_submission_1.id,
    exercise_id=exercise_1.id,
    answer=multiple_choice_answer_1,
    score=1,
)

exercise_submission_6 = ExerciseSubmission(
    id=uuid4(),
    user_id=test_taker_2.id,
    assessment_submission_id=assessment_submission_1.id,
    exercise_id=exercise_2.id,
    answer=multiple_choice_answer_2,
    score=0
)
