from typing import Dict, List, Sequence
from dataclasses import dataclass

from .multiple_choice import MultipleChoice


@dataclass(frozen=True)
class Assessment:
    name: str
    items: Sequence[MultipleChoice]

    def score(self, submission: Dict[int, List[int]]):
        result = 0
        for item_id, answer in submission.items():
            result += self.items[item_id].score(answer)
        return result
