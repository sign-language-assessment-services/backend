from dataclasses import dataclass, field

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation


@dataclass(frozen=True)
class MultimediaFile:
    location: MinioLocation
    type: MediaType
    url: str = field(default="")
