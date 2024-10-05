from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation


@dataclass(frozen=True)
class MultimediaChoice:
    location: MinioLocation
    is_correct: bool
    type: MediaType
    url: str = field(default="")

    id: UUID = field(default_factory=lambda: uuid4())
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
