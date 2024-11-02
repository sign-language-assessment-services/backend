from typing import Type

from app.core.models.assessment import Assessment
from app.database.tables.assessments import DbAssessment
from app.database.tables.exercises import DbExercise
from app.database.tables.primers import DbPrimer
from app.mappers.exercise_mapper import ExerciseMapper
from app.mappers.primer_mapper import PrimerMapper


class AssessmentMapper:
    @staticmethod
    def db_to_domain(db_assessment: Type[DbAssessment]) -> Assessment:
        items = []
        for item in db_assessment.tasks:
            if isinstance(item, DbPrimer):
                items.append(PrimerMapper.db_to_domain(item))
            elif isinstance(item, DbExercise):
                items.append(ExerciseMapper.db_to_domain(item))

        return Assessment(
            id=db_assessment.id,
            created_at=db_assessment.created_at,
            name=db_assessment.name,
            items=items
        )

    @staticmethod
    def domain_to_db(assessment: Assessment) -> DbAssessment:
        return DbAssessment(
            name=assessment.name,
            tasks=assessment.items
        )
