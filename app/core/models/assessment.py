from typing import Sequence
from dataclasses import dataclass

from .multiple_choice import MultipleChoice


@dataclass(frozen=True)
class Assessment:
    name: str
    items: Sequence[MultipleChoice]
