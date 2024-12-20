from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.core.models.submission import Submission
from app.database.tables.submissions import DbSubmission
from app.mappers.exercise_mapper import exercise_to_db, exercise_to_domain


def submission_to_domain(db_submission: DbSubmission) -> Submission:
    return Submission(
        id=db_submission.id,
        created_at=db_submission.created_at,
        user_name=db_submission.user_name,
        exercise=exercise_to_domain(db_submission.exercise),
        answer=MultipleChoiceAnswer(choices=db_submission.choices)
    )


def submission_to_db(submission: Submission) -> DbSubmission:
    return DbSubmission(
        user_name=submission.user_name,
        exercise=exercise_to_db(submission.exercise),
        choices=submission.answer.choices
    )
