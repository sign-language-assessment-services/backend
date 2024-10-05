from dataclasses import dataclass
from typing import Sequence

from app.core.models.exceptions import ChoiceNotFound
from app.core.models.exercise import Exercise


@dataclass(frozen=True)
class MultipleChoice(Exercise):
    def score(self, selected_answers: list[str]) -> int:
        self.__validate_input(selected_choice_ids=selected_answers)
        correct_answers = {str(choice.id) for choice in self.choices if choice.is_correct}
        if correct_answers == set(selected_answers):
            return 1
        return 0

    def __validate_input(self, selected_choice_ids: Sequence[str]) -> None:
        valid_choice_ids = {str(choice.id) for choice in self.choices}
        for selected_choice_id in selected_choice_ids:
            if selected_choice_id not in valid_choice_ids:
                raise ChoiceNotFound(f"The selected choice {selected_choice_id} does not exist.")
