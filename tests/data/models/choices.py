from uuid import uuid4

from app.core.models.choice import Choice
from tests.data.models.multimedia_files import (
    multimedia_file_choice_1, multimedia_file_choice_2, multimedia_file_choice_3,
    multimedia_file_choice_4, multimedia_file_choice_5, multimedia_file_choice_6, multimedia_file_choice_7,
    multimedia_file_choice_8
)

choice_1 = Choice(
    id=uuid4(),
    is_correct=True,
    content=multimedia_file_choice_1
)

choice_2 = Choice(
    id=uuid4(),
    is_correct=False,
    content=multimedia_file_choice_2
)

choice_3 = Choice(
    id=uuid4(),
    is_correct=False,
    content=multimedia_file_choice_3
)

choice_4 = Choice(
    id=uuid4(),
    is_correct=False,
    content=multimedia_file_choice_4
)

choice_5 = Choice(
    id=uuid4(),
    is_correct=True,
    content=multimedia_file_choice_5
)

choice_6 = Choice(
    id=uuid4(),
    is_correct=False,
    content=multimedia_file_choice_6
)

choice_7 = Choice(
    id=uuid4(),
    is_correct=False,
    content=multimedia_file_choice_7
)

choice_8 = Choice(
    id=uuid4(),
    is_correct=False,
    content=multimedia_file_choice_8
)
