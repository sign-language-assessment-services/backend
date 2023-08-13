from dataclasses import dataclass, field

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation


@dataclass(frozen=True)
class MultimediaChoice:
    location: MinioLocation
    is_correct: bool
    type: MediaType
    url: str = field(default="")
