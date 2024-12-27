from collections import Counter
from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.exercise import Exercise
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.core.models.score import Score
from app.repositories.submissions import list_submissions_for_user
from app.services.assessment_service import AssessmentService
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
    def score_assessment(assessment: Assessment, user_name: UUID) -> Score:
        score = Score(points=0, maximum_points=0)
        assessmentService = AssessmentService()
        submissions = list_submissions_for_user(user_name=user_name)
        for exercise in assessment.exercises:
            score.points += self.score_exercise(exercise=exercise, answer=assessment.answers[exercise.id]).points
            score.maximum_points += exercise.points
        return score
