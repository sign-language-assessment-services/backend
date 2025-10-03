import logging
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

logger = logging.getLogger(__name__)


def get_task(session: Session, _id: UUID) -> Primer | Exercise | None:
    result = get_by_id(session, DbTask, _id)
    if result:
        if result.task_type == "primer":
            logger.info(
                "Requesting task 'primer' %(_id)s with session id %(session_id)s.",
                {"_id": _id, "session_id": id(session)}
            )
            db_primer = get_by_id(session, DbPrimer, _id)
            return primer_to_domain(db_primer)
        if result.task_type == "exercise":
            logger.info(
                "Requesting task 'exercise' %(_id)s with session id %(session_id)s.",
                {"_id": _id, "session_id": id(session)}
            )
            db_exercise = get_by_id(session, DbExercise, _id)
            return exercise_to_domain(db_exercise)
    return None
