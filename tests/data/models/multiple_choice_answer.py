from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from tests.data.models.choices import choice_1, choice_2

multiple_choice_answer_1 = MultipleChoiceAnswer(
    choices=[choice_1.id]
)

multiple_choice_answer_2 = MultipleChoiceAnswer(
    choices=[choice_2.id]
)
