from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.models.static_item import StaticItem


@dataclass(frozen=True)
class Primer(StaticItem):
    assessment_id: UUID
    multimedia_file_id: UUID

    id: UUID = field(default_factory=lambda: uuid4())
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
