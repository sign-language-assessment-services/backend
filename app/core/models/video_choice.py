from dataclasses import dataclass, field

from app.core.models.minio_location import MinioLocation


@dataclass(frozen=True)
class VideoChoice:
    location: MinioLocation
    is_correct: bool
    url: str = field(default="")
    type: str = field(default="video")
