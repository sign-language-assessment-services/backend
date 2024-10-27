from typing import Sequence

from pydantic import BaseModel

from app.core.models.choice import Choice


class MultipleChoice(BaseModel):
    choices: Sequence[Choice]
