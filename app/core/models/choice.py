from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.core.models.multimedia_file import MultimediaFile


class MultipleChoiceUsage(BaseModel):
    id: UUID

    position: int = Field(default=None, ge=1, le=4)


class Choice(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime | None = Field(default=None)

    multiple_choices: list[MultipleChoiceUsage] = Field(default_factory=list)
    content: MultimediaFile | None = Field(default=None)

    is_correct: bool | None = Field(default=None)
    position: int | None = Field(default=None, ge=1, le=4)
