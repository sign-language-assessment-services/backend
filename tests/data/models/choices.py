from uuid import uuid4

from app.core.models.choice import AssociatedChoice, Choice
from tests.data.models.multimedia_files import (
    multimedia_file_choice_1, multimedia_file_choice_2, multimedia_file_choice_3,
    multimedia_file_choice_4, multimedia_file_choice_5, multimedia_file_choice_6,
    multimedia_file_choice_7, multimedia_file_choice_8
)

choice_1 = Choice(
    id=uuid4(),
    content=multimedia_file_choice_1
)

choice_2 = Choice(
    id=uuid4(),
    content=multimedia_file_choice_2
)

choice_3 = Choice(
    id=uuid4(),
    content=multimedia_file_choice_3
)

choice_4 = Choice(
    id=uuid4(),
    content=multimedia_file_choice_4
)

choice_5 = Choice(
    id=uuid4(),
    content=multimedia_file_choice_5
)

choice_6 = Choice(
    id=uuid4(),
    content=multimedia_file_choice_6
)

choice_7 = Choice(
    id=uuid4(),
    content=multimedia_file_choice_7
)

choice_8 = Choice(
    id=uuid4(),
    content=multimedia_file_choice_8
)


associated_choice_1 = AssociatedChoice(
    **choice_1.__dict__,
    position=1,
    is_correct=True
)

associated_choice_2 = AssociatedChoice(
    **choice_2.__dict__,
    position=2,
    is_correct=False
)

associated_choice_3 = AssociatedChoice(
    **choice_3.__dict__,
    position=3,
    is_correct=False
)

associated_choice_4 = AssociatedChoice(
    **choice_4.__dict__,
    position=4,
    is_correct=False
)

associated_choice_5 = AssociatedChoice(
    **choice_5.__dict__,
    position=1,
    is_correct=True
)

associated_choice_6 = AssociatedChoice(
    **choice_6.__dict__,
    position=2,
    is_correct=False
)

associated_choice_7 = AssociatedChoice(
    **choice_7.__dict__,
    position=3,
    is_correct=False
)

associated_choice_8 = AssociatedChoice(
    **choice_8.__dict__,
    position=4,
    is_correct=False
)
