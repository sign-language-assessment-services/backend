from dataclasses import dataclass

from app.core.models.multimedia_file import MultimediaFile


@dataclass(frozen=True)
class StaticItem:
    content: MultimediaFile
    position: int
