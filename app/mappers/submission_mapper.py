from typing import Type

from app.core.models.answer import Answer
from app.core.models.submission import Submission
from app.database.tables.multiple_choice_submissions import DbMultipleChoiceSubmission
from app.mappers.choice_mapper import ChoiceMapper
from app.mappers.exercise_mapper import ExerciseMapper


# Note: Currently, only multiple choice submissions are supported. It is recommended
#       to add more summission models on domain model side if more will come and
#       rename this Submission domain model to MultipleChoiceSubmission or similar.

class SubmissionMapper:
    @staticmethod
    def db_to_domain(db_submission: Type[DbMultipleChoiceSubmission]) -> Submission:
        return Submission(
            id=db_submission.id,
            created_at=db_submission.created_at,
            user_id=db_submission.user_name,
            exercise=ExerciseMapper.db_to_domain(db_submission.exercise),
            answer=Answer(
                choices=[ChoiceMapper.db_to_domain(choice) for choice in db_submission.choices]
            )
        )

    @staticmethod
    def domain_to_db(submission: Submission) -> DbMultipleChoiceSubmission:
        return DbMultipleChoiceSubmission(
            user_name=submission.user_id,
            exercise=submission.exercise,
            choices=submission.answer.choices
        )
