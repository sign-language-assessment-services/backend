from __future__ import annotations

from enum import Enum

from app.core.models.exceptions import UnsupportedMimeType


class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"

    @classmethod
    def from_content_type(cls, content_type: str) -> MediaType:
        if content_type.startswith("video"):
            return cls.VIDEO
        if content_type.startswith("image"):
            return cls.IMAGE
        raise UnsupportedMimeType("Only images or videos are supported.")
