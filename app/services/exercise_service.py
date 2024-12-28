from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.exercise import Exercise
from app.repositories.exercises import get_exercise, list_exercises
from app.settings import get_settings


class ExerciseService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def get_exercise_by_id(session: Session, exercise_id: UUID) -> Exercise | None:
        return get_exercise(session=session, _id=exercise_id)

    @staticmethod
    def list_exercises(session: Session) -> list[Exercise]:
        return list_exercises(session=session)
