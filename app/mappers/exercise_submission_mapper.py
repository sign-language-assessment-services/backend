from app.core.models.exercise_submission import ExerciseSubmission
from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.database.tables.exercise_submissions import DbExerciseSubmission


def exercise_submission_to_domain(db_submission: DbExerciseSubmission) -> ExerciseSubmission:
    return ExerciseSubmission(
        id=db_submission.id,
        created_at=db_submission.created_at,
        user_id=db_submission.user_id,
        answer=MultipleChoiceAnswer(choices=db_submission.choices),
        score=db_submission.score,
        assessment_submission_id=db_submission.assessment_submission_id,
        exercise_id=db_submission.exercise_id
    )


def exercise_submission_to_db(submission: ExerciseSubmission) -> DbExerciseSubmission:
    return DbExerciseSubmission(
        id=submission.id,
        created_at=submission.created_at,
        user_id=submission.user_id,
        choices=submission.answer.choices,
        score=submission.score,
        assessment_submission_id=submission.assessment_submission_id,
        exercise_id=submission.exercise_id
    )
