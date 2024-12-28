from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.core.models.submission import Submission
from app.database.tables.submissions import DbSubmission


def submission_to_domain(db_submission: DbSubmission) -> Submission:
    return Submission(
        id=db_submission.id,
        created_at=db_submission.created_at,
        user_name=db_submission.user_name,
        assessment_id=db_submission.assessment_id,
        exercise_id=db_submission.exercise_id,
        multiple_choice_id=db_submission.multiple_choice_id,
        answer=MultipleChoiceAnswer(choices=db_submission.choices)
    )


def submission_to_db(submission: Submission) -> DbSubmission:
    return DbSubmission(
        id=submission.id,
        created_at=submission.created_at,
        user_name=submission.user_name,
        assessment_id=submission.assessment_id,
        exercise_id=submission.exercise_id,
        multiple_choice_id=submission.multiple_choice_id,
        choices=submission.answer.choices
    )
