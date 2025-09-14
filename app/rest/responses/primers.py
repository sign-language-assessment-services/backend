from uuid import UUID

from pydantic import BaseModel, Field, computed_field

from app.core.models.multimedia_file import MultimediaFile


class CreatePrimerResponse(BaseModel):
    id: UUID
    content: MultimediaFile = Field(exclude=True)

    @computed_field(
        description="The id of the multimedia file",
        json_schema_extra={
            "example": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
    )
    @property
    def multimedia_file_id(self) -> UUID:
        return self.content.id  # pylint: disable=no-member


class GetPrimerResponse(BaseModel):
    id: UUID
    content: MultimediaFile = Field(exclude=True)

    @computed_field(
        description="Media type of the multimedia file",
        json_schema_extra={
            "example": "IMAGE"
        }
    )
    @property
    def media_type(self) -> str:
        return self.content.media_type.value  # pylint: disable=no-member

    @computed_field(
        description="The id of the multimedia file",
        json_schema_extra={
            "example": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
    )
    @property
    def multimedia_file_id(self) -> str:
        return str(self.content.id)  # pylint: disable=no-member


class ListPrimerResponse(BaseModel):
    id: UUID
    content: MultimediaFile = Field(exclude=True)

    @computed_field(
        description="Media type of the multimedia file",
        json_schema_extra={
            "example": "IMAGE"
        }
    )
    @property
    def media_type(self) -> str:
        return self.content.media_type.value  # pylint: disable=no-member
