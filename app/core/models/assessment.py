from dataclasses import dataclass
from typing import Sequence

from app.core.models.exceptions import UnexpectedItemType
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.static_item import StaticItem


@dataclass(frozen=True)
class Assessment:
    name: str
    items: Sequence[MultipleChoice | StaticItem]

    def score(self, submission: dict[int, list[int]]) -> dict[str, int]:
        result = 0
        for item_id, answer in submission.items():
            item = self.items[item_id]
            if not isinstance(item, MultipleChoice):
                raise UnexpectedItemType(
                    f"Only multiple choice is allowed. Got {type(self.items[item_id])}"
                )
            result += item.score(answer)
        return {"score": result}
