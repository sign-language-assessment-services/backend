import logging

logger = logging.getLogger(__name__)


def import_tables() -> None:
    """Tables have to be imported in declarative mapping style"""
    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.database.tables.assessment_submissions import DbAssessmentSubmission
    from app.database.tables.assessments import DbAssessment
    from app.database.tables.assessments_tasks import DbAssessmentsTasks
    from app.database.tables.bucket_objects import DbBucketObjects
    from app.database.tables.choices import DbChoice
    from app.database.tables.exercise_submissions import DbExerciseSubmission
    from app.database.tables.exercises import DbExercise
    from app.database.tables.multiple_choices import DbMultipleChoice
    from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
    from app.database.tables.primers import DbPrimer
    from app.database.tables.tasks import DbTask

    _ = (  # use imports to prevent them automatically stripped away by IDE
        DbAssessment, DbAssessmentSubmission, DbAssessmentsTasks,
        DbBucketObjects, DbChoice, DbExercise, DbExerciseSubmission,
        DbMultipleChoice, DbMultipleChoicesChoices, DbPrimer, DbTask
    )
