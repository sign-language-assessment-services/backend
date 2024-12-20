from app.core.models.assessment import Assessment
from app.database.tables.assessments import DbAssessment
from app.database.tables.exercises import DbExercise
from app.database.tables.primers import DbPrimer
from app.mappers.exercise_mapper import exercise_to_db, exercise_to_domain
from app.mappers.primer_mapper import primer_to_db, primer_to_domain


def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
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
        tasks=tasks
    )


def assessment_to_db(assessment: Assessment) -> DbAssessment:
    tasks = []
    for task in assessment.tasks:
        if isinstance(task, DbPrimer):
            tasks.append(primer_to_db(task))
        elif isinstance(task, DbExercise):
            tasks.append(exercise_to_db(task))

    return DbAssessment(
        id=assessment.id,
        created_at=assessment.created_at,
        name=assessment.name,
        tasks=tasks
    )
