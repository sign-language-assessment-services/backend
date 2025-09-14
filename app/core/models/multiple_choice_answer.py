from uuid import UUID

from pydantic import BaseModel


class MultipleChoiceAnswer(BaseModel):
    choices: list[UUID]
