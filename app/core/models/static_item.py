from dataclasses import dataclass

from app.core.models.multimedia import Multimedia


@dataclass(frozen=True)
class StaticItem:
    content: Multimedia
    position: int


# TODO: -> moved to primer.py (obsolete)?
