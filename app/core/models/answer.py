from typing import Sequence

from pydantic import BaseModel

from app.core.models.choice import Choice


class Answer(BaseModel):
    choices: Sequence[Choice] | str
