from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.core.models.multimedia_file import MultimediaFile


class Primer(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime | None = Field(default=None)

    content: MultimediaFile
