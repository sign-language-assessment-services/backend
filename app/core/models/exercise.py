from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.core.models.multimedia_file import MultimediaFile
from app.core.models.multiple_choice import MultipleChoice


class Exercise(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    question: MultimediaFile
    answer: MultipleChoice
