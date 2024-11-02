from pydantic import BaseModel

from app.core.models.choice import Choice


class Answer(BaseModel):
    choices: list[Choice]
