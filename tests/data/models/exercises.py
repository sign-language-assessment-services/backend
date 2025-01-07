from uuid import uuid4

from app.core.models.exercise import Exercise
from app.core.models.question_type import QuestionType
from tests.data.models.multiple_choices import multiple_choice_1, multiple_choice_2
from tests.data.models.questions import question_1, question_2

exercise_1 = Exercise(
    id=uuid4(),
    points=1,
    question=question_1,
    question_type=QuestionType(content=multiple_choice_1)
)

exercise_2 = Exercise(
    id=uuid4(),
    points=1,
    question=question_2,
    question_type=QuestionType(content=multiple_choice_2)
)
