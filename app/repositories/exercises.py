from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.exercise import Exercise
from app.database.tables.exercises import DbExercise
from app.mappers.exercise_mapper import exercise_to_db, exercise_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry


def add_exercise(session: Session, exercise: Exercise) -> None:
    db_model = exercise_to_db(exercise)
    add_entry(session, db_model)


def get_exercise(session: Session, _id: UUID) -> Exercise | None:
    result = get_by_id(session, DbExercise, _id)
    if result:
        return exercise_to_domain(result)


def list_exercises(session: Session) -> list[Exercise]:
    results = get_all(session, DbExercise)
    return [exercise_to_domain(result) for result in results]


def update_exercise(session: Session, _id: UUID, **kwargs: Any) -> None:
    update_entry(session, DbExercise, _id, **kwargs)


def delete_exercise(session: Session, _id: UUID) -> None:
    delete_entry(session, DbExercise, _id)
