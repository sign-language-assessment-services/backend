from app.core.models.multiple_choice import MultipleChoice
from tests.data.models.choices import (
    associated_choice_1, associated_choice_2, associated_choice_3, associated_choice_4,
    associated_choice_5, associated_choice_6, associated_choice_7, associated_choice_8
)

multiple_choice_1 = MultipleChoice(
    choices=[associated_choice_1, associated_choice_2, associated_choice_3, associated_choice_4]
)

multiple_choice_2 = MultipleChoice(
    choices=[associated_choice_5, associated_choice_6, associated_choice_7, associated_choice_8]
)
