from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from tests.data.models.choices import associated_choice_1, associated_choice_2

multiple_choice_answer_1 = MultipleChoiceAnswer(
    choices=[associated_choice_1.id]
)

multiple_choice_answer_2 = MultipleChoiceAnswer(
    choices=[associated_choice_2.id]
)
