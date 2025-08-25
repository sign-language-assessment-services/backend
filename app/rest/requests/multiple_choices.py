from uuid import UUID

from pydantic import BaseModel, Field


class CorrectChoice(BaseModel):
    id: UUID
    is_correct: bool = Field(default=False)


class CreateMultipleChoiceRequest(BaseModel):
    choices: list[CorrectChoice]
