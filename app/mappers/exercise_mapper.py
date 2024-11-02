from app.core.models.exercise import Exercise
from app.database.tables.exercises import DbExercise
from app.mappers.multimedia_file_mapper import MultimediaFileMapper
from app.mappers.multiple_choice_mapper import MultipleChoiceMapper


class ExerciseMapper:
    @staticmethod
    def db_to_domain(db_exercise: DbExercise) -> Exercise:
        return Exercise(
            id=db_exercise.id,
            created_at=db_exercise.created_at,
            question=MultimediaFileMapper.db_to_domain(db_exercise.bucket),
            answer=MultipleChoiceMapper.db_to_domain(db_exercise.multiple_choice)
        )
