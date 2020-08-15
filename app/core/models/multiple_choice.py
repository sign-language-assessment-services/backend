from dataclasses import dataclass
from typing import Sequence

from .choice import Choice


@dataclass(frozen=True)
class MultipleChoice:
    description: str
    choices: Sequence[Choice]
