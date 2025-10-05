import logging
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.exercise import Exercise
from app.core.models.question import Question
from app.core.models.question_type import QuestionType
from app.repositories.exercises import add_exercise, get_exercise, list_exercises
from app.repositories.multimedia_files import get_multimedia_file
from app.repositories.multiple_choices import get_multiple_choice

logger = logging.getLogger(__name__)


class ExerciseService:
    @staticmethod
    def create_exercise(session: Session, points: int, multimedia_file_id: UUID, multiple_choice_id: UUID) -> Exercise:
        multimedia_file = get_multimedia_file(session=session, _id=multimedia_file_id)
        multiple_choice = get_multiple_choice(session=session, _id=multiple_choice_id)
        exercise = Exercise(
            points=points,
            question=Question(content=multimedia_file),
            question_type=QuestionType(content=multiple_choice)
        )
        add_exercise(session=session, exercise=exercise)
        return exercise


    @staticmethod
    def get_exercise_by_id(session: Session, exercise_id: UUID) -> Exercise | None:
        logger.info(
            "Trying to receive exercise %(_id)s with session id %(session_id)s.",
            {"_id": exercise_id, "session_id": id(session)}
        )
        return get_exercise(session=session, _id=exercise_id)

    @staticmethod
    def list_exercises(session: Session) -> list[Exercise]:
        return list_exercises(session=session)
