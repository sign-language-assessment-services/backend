from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer


class Assessment(BaseModel):
    id: UUID = Field(default_factory=UUID)
    created_at: datetime = Field(default_factory=datetime.now)

    name: str
    items: list[Primer | Exercise] = Field(default_factory=list)
