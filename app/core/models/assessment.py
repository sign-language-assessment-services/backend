from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer


class Assessment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    name: str
    deadline: datetime | None = Field(default=None)
    max_attempts: int | None = Field(default=None)
    tasks: list[Primer | Exercise] = Field(default_factory=list)
