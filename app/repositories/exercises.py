import logging
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.exercise import Exercise
from app.database.tables.exercises import DbExercise
from app.mappers.exercise_mapper import exercise_to_db, exercise_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry

logger = logging.getLogger(__name__)


def add_exercise(session: Session, exercise: Exercise) -> None:
    db_model = exercise_to_db(exercise)
    logger.info(
        "Requesting add exercise %(_id)s with session id %(session_id)s.",
        {"_id": db_model.id, "session_id": id(session)}
    )
    add_entry(session, db_model)


def get_exercise(session: Session, _id: UUID) -> Exercise | None:
    logger.info(
        "Requesting exercise %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    result = get_by_id(session, DbExercise, _id)
    if result:
        return exercise_to_domain(result)
    return None


def list_exercises(session: Session) -> list[Exercise]:
    logger.info(
        "Requesting all exercises with session id %(session_id)s.",
        {"session_id": id(session)}
    )
    results = get_all(session, DbExercise)
    return [exercise_to_domain(result) for result in results]


def update_exercise(session: Session, _id: UUID, **kwargs: Any) -> None:
    logger.info(
        "Requesting update exercise %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    update_entry(session, DbExercise, _id, **kwargs)


def delete_exercise(session: Session, _id: UUID) -> None:
    logger.info(
        "Requesting delete exercise %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    delete_entry(session, DbExercise, _id)
