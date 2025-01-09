from uuid import uuid4

from app.core.models.submission import Submission
from tests.data.models.assessments import assessment_1
from tests.data.models.exercises import exercise_1, exercise_2
from tests.data.models.multiple_choice_answer import (
    multiple_choice_answer_1, multiple_choice_answer_2
)
from tests.data.models.users import test_taker_1, test_taker_2

submission_1 = Submission(
    id=uuid4(),
    user_id=test_taker_1.id,
    assessment_id=assessment_1.id,
    exercise_id=exercise_1.id,
    multiple_choice_id=exercise_1.question_type.content.id,
    answer=multiple_choice_answer_1,
)

submission_2 = Submission(
    id=uuid4(),
    user_id=test_taker_1.id,
    assessment_id=assessment_1.id,
    exercise_id=exercise_1.id,
    multiple_choice_id=exercise_1.question_type.content.id,
    answer=multiple_choice_answer_2,
)

submission_3 = Submission(
    id=uuid4(),
    user_id=test_taker_1.id,
    assessment_id=assessment_1.id,
    exercise_id=exercise_2.id,
    multiple_choice_id=exercise_2.question_type.content.id,
    answer=multiple_choice_answer_1,
)

submission_4 = Submission(
    id=uuid4(),
    user_id=test_taker_1.id,
    assessment_id=assessment_1.id,
    exercise_id=exercise_2.id,
    multiple_choice_id=exercise_2.question_type.content.id,
    answer=multiple_choice_answer_2,
)

submission_5 = Submission(
    id=uuid4(),
    user_id=test_taker_2.id,
    assessment_id=assessment_1.id,
    exercise_id=exercise_1.id,
    multiple_choice_id=exercise_1.question_type.content.id,
    answer=multiple_choice_answer_1,
)

submission_6 = Submission(
    id=uuid4(),
    user_id=test_taker_2.id,
    assessment_id=assessment_1.id,
    exercise_id=exercise_2.id,
    multiple_choice_id=exercise_1.question_type.content.id,
    answer=multiple_choice_answer_2,
)
