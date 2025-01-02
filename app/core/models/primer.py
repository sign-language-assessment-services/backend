from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field

from app.core.models.multimedia_file import MultimediaFile


class Primer(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    content: MultimediaFile


class PrimerResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    content: MultimediaFile = Field(exclude=True)

    @computed_field
    @property
    def url(self) -> str:
        return "http://example.com/primer.mp4"

    @computed_field
    @property
    def media_type(self) -> str:
        return self.content.media_type.value
