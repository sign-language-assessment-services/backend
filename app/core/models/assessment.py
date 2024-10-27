from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer


@dataclass(frozen=True)
class Assessment:
    name: str
    items: list[Primer | Exercise] = field(default_factory=list)

    id: UUID = field(default_factory=lambda: uuid4())
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
