from dataclasses import dataclass
from typing import Sequence

from app.core.models.multiple_choice import MultipleChoice


@dataclass(frozen=True)
class Assessment:
    name: str
    items: Sequence[MultipleChoice]

    def score(self, submission: dict[int, list[int]]) -> dict[str, int]:
        result = 0
        for item_id, answer in submission.items():
            result += self.items[item_id].score(answer)
        return {"score": result}
