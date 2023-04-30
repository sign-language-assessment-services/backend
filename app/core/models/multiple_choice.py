from dataclasses import dataclass
from typing import Sequence

from app.core.models.text_choice import TextChoice
from app.core.models.text_question import TextQuestion
from app.core.models.video_choice import VideoChoice
from app.core.models.video_question import VideoQuestion


@dataclass(frozen=True)
class MultipleChoice:
    question: TextQuestion | VideoQuestion
    choices: Sequence[TextChoice | VideoChoice]

    def score(self, selected_answers: Sequence[int]) -> int:
        self.__validate_input(selected_answers)
        correct_answers = {
            index for index, choice in enumerate(self.choices)
            if choice.is_correct
        }
        if correct_answers == set(selected_answers):
            return 1
        return 0

    def __validate_input(self, selected_answers: Sequence[int]) -> None:
        if selected_answers:
            if max(selected_answers) >= len(self.choices) or min(
                    selected_answers) < 0:
                raise ValueError("A selected answer does not exist.")
