from app.core.models.exercise import Exercise
from app.core.models.exercise_submission import ExerciseSubmission
from app.core.models.multiple_choice import MultipleChoice


class ScoringService:
    def score(self, exercise_submission: ExerciseSubmission, exercise: Exercise) -> None:
        if isinstance(exercise.question_type.content, MultipleChoice):
            self.score_multiple_choice(exercise=exercise, exercise_submission=exercise_submission)

    @staticmethod
    def score_multiple_choice(
            exercise: Exercise,
            exercise_submission: ExerciseSubmission,
    ) -> None:
        choices = exercise.question_type.content.choices
        correct_choices = [choice.id for choice in choices if choice.is_correct]

        if exercise_submission.answer.choices == correct_choices:
            exercise_submission.score = exercise.points
        else:
            exercise_submission.score = 0
