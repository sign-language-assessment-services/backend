# pylint: disable=R0801

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.core.models.multimedia_file import MultimediaFile


@dataclass(frozen=True)
class Primer:
    position: int

    assessment_id: str
    multimedia_file_id: str | None

    content: MultimediaFile | None

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
