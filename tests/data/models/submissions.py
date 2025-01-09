from uuid import uuid4

from app.core.models.submission import Submission
from tests.data.models.assessments import assessment_1
from tests.data.models.exercises import exercise_1
from tests.data.models.multiple_choice_answer import (
    multiple_choice_answer_1, multiple_choice_answer_2
)
from tests.data.models.multiple_choices import multiple_choice_1

submission_1 = Submission(
    id=uuid4(),
    user_id=uuid4(),
    assessment_id=assessment_1.id,
    exercise_id=exercise_1.id,
    multiple_choice_id=multiple_choice_1.id,
    answer=multiple_choice_answer_1
)

submission_2 = Submission(
    id=uuid4(),
    user_id=uuid4(),
    assessment_id=assessment_1.id,
    exercise_id=exercise_1.id,
    multiple_choice_id=multiple_choice_1.id,
    answer=multiple_choice_answer_2
)
