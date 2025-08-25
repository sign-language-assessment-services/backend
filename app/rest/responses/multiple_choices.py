from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.core.models.multimedia_file import MultimediaFile


class CreateMultipleChoiceResponse(BaseModel):
    id: UUID


class GetMultipleChoiceResponse(BaseModel):
    id: UUID
    content: list[MultimediaFile] = Field(exclude=True)

    @field_validator("choice_ids", mode="before")
    @classmethod
    def compute_choice_ids(cls, value) -> list[UUID]:
        return [choice.id for choice in value.content]


class ListMultipleChoiceResponse(BaseModel):
    id: UUID
