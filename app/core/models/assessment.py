import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.core.models.exceptions import UnexpectedItemType
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.score import Score
from app.core.models.static_item import StaticItem


@dataclass(frozen=True)
class Assessment:
    name: str
    items: list[MultipleChoice | StaticItem] = field(default_factory=list)

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))

    def score(self, answers: dict[str, list[str]]) -> Score:
        points = 0
        max_points = self._get_maximum_points()
        for item_id, answer in answers.items():
            item = self.items[item_id]
            if not isinstance(item, MultipleChoice):
                raise UnexpectedItemType(
                    f"Only multiple choice is allowed. Got {type(item)}"
                )
            points += item.score(answer)
        return Score(points=points, maximum_points=max_points)

    def _get_maximum_points(self) -> int:
        return len([item for item in self.items if not isinstance(item, StaticItem)])
