from dataclasses import dataclass
from typing import Sequence

from .text_choice import TextChoice
from .video_choice import VideoChoice


@dataclass(frozen=True)
class MultipleChoice:
    description: str
    choices: Sequence[TextChoice | VideoChoice]

    def score(self, selected_answers: Sequence[int]):
        self.__validate_input(selected_answers)
        correct_answers = {
            index for index, choice in enumerate(self.choices)
            if choice.is_correct
        }
        if correct_answers == set(selected_answers):
            return 1
        return 0

    def __validate_input(self, selected_answers):
        if selected_answers:
            if max(selected_answers) >= len(self.choices) or min(
                    selected_answers) < 0:
                raise ValueError("A selected answer does not exist.")
