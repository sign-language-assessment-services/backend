from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.core.models.choice import Choice


class MultipleChoice(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    choices: list[Choice] = Field(default_factory=list)
