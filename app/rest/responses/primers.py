from uuid import UUID, uuid4

from pydantic import BaseModel, computed_field, Field

from app.core.models.multimedia_file import MultimediaFile


class PrimerResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    content: MultimediaFile = Field(exclude=True)

    @computed_field
    @property
    def media_type(self) -> str:
        return self.content.media_type.value  # pylint: disable=no-member

    @computed_field
    @property
    def multimedia_file_id(self) -> str:
        return str(self.content.id)  # pylint: disable=no-member
