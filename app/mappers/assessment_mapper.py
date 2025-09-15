import logging

from app.core.models.assessment import Assessment
from app.core.models.exercise import Exercise
from app.core.models.primer import Primer
from app.database.tables.assessments import DbAssessment
from app.database.tables.exercises import DbExercise
from app.database.tables.primers import DbPrimer
from app.mappers.exercise_mapper import exercise_to_db, exercise_to_domain
from app.mappers.primer_mapper import primer_to_db, primer_to_domain

logger = logging.getLogger(__name__)


def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    logger.debug(
        "Mapping assessment to domain model: %(db_assessment)r",
        {"db_assessment": db_assessment}
    )
    tasks = []
    for task in db_assessment.tasks:
        if isinstance(task, DbPrimer):
            tasks.append(primer_to_domain(task))
        elif isinstance(task, DbExercise):
            tasks.append(exercise_to_domain(task))

    return Assessment(
        id=db_assessment.id,
        created_at=db_assessment.created_at,
        name=db_assessment.name,
        deadline=db_assessment.deadline,
        max_attempts=db_assessment.max_attempts,
        tasks=tasks
    )


def assessment_to_db(assessment: Assessment) -> DbAssessment:
    logger.debug(
        "Mapping assessment to database model: %(assessment)r",
        {"assessment": assessment}
    )
    tasks = []
    for task in assessment.tasks:
        if isinstance(task, Primer):
            tasks.append(primer_to_db(task))
        elif isinstance(task, Exercise):
            tasks.append(exercise_to_db(task))

    return DbAssessment(
        id=assessment.id,
        created_at=assessment.created_at,
        name=assessment.name,
        deadline=assessment.deadline,
        max_attempts=assessment.max_attempts,
        tasks=tasks,
    )
