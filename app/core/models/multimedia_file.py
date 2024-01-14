from dataclasses import dataclass, field

from app.core.models.media_types import MediaType


@dataclass(frozen=True)
class MultimediaFile:
    bucket: str
    key: str
    type: MediaType
    url: str = field(default="")
