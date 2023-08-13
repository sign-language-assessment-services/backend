from dataclasses import dataclass

from app.core.models.video import Video


@dataclass(frozen=True)
class StaticItem:
    content: Video
    position: int
