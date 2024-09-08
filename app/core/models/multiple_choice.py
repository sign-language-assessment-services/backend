from dataclasses import dataclass
from typing import Sequence

from app.core.models.multimedia import Multimedia
from app.core.models.multimedia_choice import MultimediaChoice
from app.type_hints import SelectedAnswers


@dataclass(frozen=True)
class MultipleChoice:
    question: Multimedia
    choices: Sequence[MultimediaChoice]
    position: int

    def score(self, selected_answers: SelectedAnswers) -> int:
        # TODO: use real id for choice_id (not position as choice_id)
        selected_answers = [int(c) for c in selected_answers.get("choice_ids", [])]
        self.__validate_input(selects=selected_answers)
        correct_answers = {
            index for index, choice in enumerate(self.choices)
            if choice.is_correct
        }
        if correct_answers == set(selected_answers):
            return 1
        return 0

    def __validate_input(self, selects: Sequence[int]) -> None:
        if selects and (
                max(selects) >= len(self.choices) or
                min(selects) < 0
        ):
            raise ValueError("A selected answer does not exist.")
