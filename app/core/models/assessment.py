from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer


class Assessment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    name: str
    tasks: list[Primer | Exercise] = Field(default_factory=list)
