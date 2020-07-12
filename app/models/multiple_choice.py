from typing import Sequence

from pydantic import BaseModel  # pylint: disable=E0611

from app.models.choice import Choice


class MultipleChoice(BaseModel):
    description: str
    choices: Sequence[Choice]
