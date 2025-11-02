import logging

from app.core.models.assessment import Assessment
from app.database.tables.assessments import DbAssessment
from app.database.tables.exercises import DbExercise
from app.database.tables.primers import DbPrimer
from app.mappers.exercise_mapper import exercise_to_domain
from app.mappers.primer_mapper import primer_to_domain

logger = logging.getLogger(__name__)


def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    logger.debug(
        "Transform assessment with id %(_id)s into domain model object.",
        {"_id": db_assessment.id}
    )

    number = 0
    tasks = []
    for number, task in enumerate(db_assessment.tasks, start=1):
        if isinstance(task, DbPrimer):
            tasks.append(primer_to_domain(task))
        elif isinstance(task, DbExercise):
            tasks.append(exercise_to_domain(task))
    logger.debug(
        "Added %(number)d tasks from database object to assessment.",
        {"number": number}
    )

    assessment = Assessment(
        id=db_assessment.id,
        created_at=db_assessment.created_at,
        name=db_assessment.name,
        deadline=db_assessment.deadline,
        max_attempts=db_assessment.max_attempts,
        tasks=tasks
    )
    return assessment


def assessment_to_db(assessment: Assessment) -> DbAssessment:
    logger.debug("Transform assessment into database object.")

    db_assessment = DbAssessment(
        id=assessment.id,
        created_at=assessment.created_at,
        name=assessment.name,
        deadline=assessment.deadline,
        max_attempts=assessment.max_attempts
    )
    logger.debug(
        "Assessment database object with id %(_id)s created.",
        {"_id": db_assessment.id}
    )
    return db_assessment
