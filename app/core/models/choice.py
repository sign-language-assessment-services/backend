from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.models.multimedia_file import MultimediaFile


class Choice(BaseModel):
    id: UUID = Field(default_factory=UUID)
    created_at: datetime = Field(default_factory=datetime.now)

    is_correct: bool
    position: int
    content: MultimediaFile
