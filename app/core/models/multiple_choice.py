from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.models.choice import Choice


class MultipleChoice(BaseModel):
    id: UUID = Field(default_factory=UUID)
    created_at: datetime = Field(default_factory=datetime.now)

    choices: list[Choice]
    random_order: bool = Field(default=False)
