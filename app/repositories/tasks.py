from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer
from app.database.tables.exercises import DbExercise
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from app.mappers.exercise_mapper import exercise_to_domain
from app.mappers.primer_mapper import primer_to_domain
from app.repositories.utils import get_by_id


def get_task(session: Session, _id: UUID) -> Primer | Exercise | None:
    result = get_by_id(session, DbTask, _id)
    if result:
        if result.task_type == "primer":
            db_primer = get_by_id(session, DbPrimer, _id)
            return primer_to_domain(db_primer)
        if result.task_type == "exercise":
            db_exercise = get_by_id(session, DbExercise, _id)
            return exercise_to_domain(db_exercise)
    return None
