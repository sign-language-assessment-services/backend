from collections import Counter
from typing import Annotated

from fastapi import Depends

from app.config import Settings
from app.core.models.exercise import Exercise
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.core.models.score import Score
from app.settings import get_settings


class ScorerService:
    def __init__(
            self,
            settings: Annotated[Settings, Depends(get_settings)],
    ):
        self.settings = settings

    @staticmethod
    def score_exercise(exercise: Exercise, answer: MultipleChoiceAnswer) -> Score:
        points = 0
        question_type = exercise.question_type.content
        if isinstance(question_type, MultipleChoice):
            if Counter(question_type.choices) == Counter(answer.choices):
                points = exercise.points
        return Score(points=points, maximum_points=exercise.points)

    @staticmethod
    def score_assessment() -> Score:
        score = Score(points=0, maximum_points=0)
        # TODO: Scoring
        return score
