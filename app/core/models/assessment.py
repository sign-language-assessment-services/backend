from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.models.exceptions import UnexpectedItemType
from app.core.models.exercise import Exercise
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.primer import Primer
from app.core.models.score import Score
from app.core.models.static_item import StaticItem
from app.type_hints import Answers


@dataclass(frozen=True)
class Assessment:
    name: str
    items: list[Primer | Exercise] = field(default_factory=list)

    id: UUID = field(default_factory=lambda: uuid4())
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))

    def score(self, answers: Answers) -> Score:
        points = 0
        max_points = self._get_maximum_points()
        for answer in answers:
            item = self.items[int(answer["item_id"])]  # TODO: replace with real id (database), yet position
            if not isinstance(item, MultipleChoice):
                raise UnexpectedItemType(
                    f"Only multiple choice is allowed. Got {type(item)}"
                )
            points += item.score(answer)
        return Score(points=points, maximum_points=max_points)

    def _get_maximum_points(self) -> int:
        # Each MultipleChoice item gives maximum 1 point, StaticItems are ignored
        return len([item for item in self.items if not isinstance(item, StaticItem)])
