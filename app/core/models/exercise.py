from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Sequence
from uuid import UUID, uuid4

from app.core.models.multimedia_choice import MultimediaChoice
from app.core.models.multimedia_file import MultimediaFile


@dataclass(frozen=True)
class Exercise:
    position: int
    question: MultimediaFile
    choices: Sequence[MultimediaChoice]

    assessment_id: UUID
    multimedia_file_id: UUID

    id: UUID = field(default_factory=lambda: uuid4())
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
