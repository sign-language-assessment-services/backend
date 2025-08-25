from uuid import UUID

from pydantic import BaseModel, Field, computed_field

from app.core.models.multimedia_file import MultimediaFile


class CreatePrimerResponse(BaseModel):
    id: UUID


class GetPrimerResponse(BaseModel):
    id: UUID
    content: MultimediaFile = Field(exclude=True)

    @computed_field
    @property
    def media_type(self) -> str:
        return self.content.media_type.value  # pylint: disable=no-member

    @computed_field
    @property
    def multimedia_file_id(self) -> str:
        return str(self.content.id)  # pylint: disable=no-member


class ListPrimerResponse(BaseModel):
    id: UUID
