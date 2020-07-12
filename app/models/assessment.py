from typing import Sequence

from pydantic import BaseModel  # pylint: disable=E0611

from app.models.multiple_choice import MultipleChoice


class Assessment(BaseModel):
    name: str
    items: Sequence[MultipleChoice]
