from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.models.exceptions import ExerciseNotFound, UnexpectedItemType
from app.core.models.exercise import Exercise
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.score import Score
from app.core.models.static_item import StaticItem


@dataclass(kw_only=True)
class Submission:
    user_id: str
    assessment_id: UUID
    answers: list[MultipleChoice | StaticItem] = field(default_factory=list)
    points: int
    maximum_points: int
    percentage: float

    id: UUID = field(default_factory=lambda: uuid4())
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))

    def score(self, answers: list[Exercise]) -> Score:
        points = 0
        max_points = self._get_maximum_points()
        for exercise_id, choice_ids in answers.items():
            choice: MultipleChoice | None = next((item for item in self.answers if str(item.id) == exercise_id), None)
            self._validate_answer(choice, exercise_id)
            points += choice.score(choice_ids)
        return Score(points=points, maximum_points=max_points)

    def _get_maximum_points(self) -> int:
        # Each MultipleChoice item gives maximum 1 point, StaticItems are ignored
        return len([item for item in self.answers if not isinstance(item, StaticItem)])

    @staticmethod
    def _validate_answer(item: Exercise | None, exercise_id: str) -> None:
        if item is None:
            raise ExerciseNotFound(f"Answer contains an invalid exercise id {exercise_id}.")
        if not isinstance(item, MultipleChoice):
            raise UnexpectedItemType(
                f"Only multiple choice is allowed. Got {type(item)}."
            )
