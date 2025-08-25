from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.core.models.multimedia_file import MultimediaFile


class CreateChoiceResponse(BaseModel):
    id: UUID


class GetChoiceResponse(BaseModel):
    id: UUID
    content: MultimediaFile = Field(exclude=True)

    @field_validator("multimedia_file_id", mode="before")
    @classmethod
    def compute_multimedia_file_id(cls, value) -> UUID:
        return value.content.id


class ListChoiceResponse(BaseModel):
    id: UUID
