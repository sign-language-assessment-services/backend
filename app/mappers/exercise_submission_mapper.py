import logging

from app.core.models.exercise_submission import ExerciseSubmission
from app.core.models.multiple_choice_answer import MultipleChoiceAnswer
from app.database.tables.exercise_submissions import DbExerciseSubmission

logger = logging.getLogger(__name__)


def exercise_submission_to_domain(db_submission: DbExerciseSubmission) -> ExerciseSubmission:
    logger.debug("Transform DbExerciseSubmission into domain model object.")
    exercise_submission = ExerciseSubmission(
        id=db_submission.id,
        created_at=db_submission.created_at,
        answer=MultipleChoiceAnswer(choices=db_submission.choices),
        score=db_submission.score,
        assessment_submission_id=db_submission.assessment_submission_id,
        exercise_id=db_submission.exercise_id
    )
    return exercise_submission


def exercise_submission_to_db(submission: ExerciseSubmission) -> DbExerciseSubmission:
    logger.debug("Transform exercise submission into database object.")
    db_exercise_submission = DbExerciseSubmission(
        id=submission.id,
        created_at=submission.created_at,
        choices=submission.answer.choices,
        score=submission.score,
        assessment_submission_id=submission.assessment_submission_id,
        exercise_id=submission.exercise_id
    )
    logger.debug(
        "Exercise submission database object with id %(_id)s created.",
        {"_id": db_exercise_submission.id}
    )
    return db_exercise_submission
