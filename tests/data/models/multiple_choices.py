from app.core.models.multiple_choice import MultipleChoice
from tests.data.models.choices import choice_1, choice_2, choice_3, choice_4, choice_5, choice_6, choice_7, choice_8

multiple_choice_1 = MultipleChoice(
    choices=[choice_1, choice_2, choice_3, choice_4]
)

multiple_choice_2 = MultipleChoice(
    choices=[choice_5, choice_6, choice_7, choice_8]
)
