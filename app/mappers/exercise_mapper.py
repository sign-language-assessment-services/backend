from app.core.models.exercise import Exercise
from app.core.models.question import Question
from app.core.models.question_type import QuestionType
from app.database.tables.exercises import DbExercise
from app.mappers.multimedia_file_mapper import bucket_object_to_domain
from app.mappers.multiple_choice_mapper import multiple_choice_to_domain


def exercise_to_domain(db_exercise: DbExercise) -> Exercise:
    return Exercise(
        id=db_exercise.id,
        created_at=db_exercise.created_at,
        points=db_exercise.points,
        question=Question(
            content=bucket_object_to_domain(db_exercise.bucket_object)
        ),
        question_type=QuestionType(
            content=multiple_choice_to_domain(db_exercise.multiple_choice)
        )
    )


def exercise_to_db(exercise: Exercise) -> DbExercise:
    return DbExercise(
        id=exercise.id,
        created_at=exercise.created_at,
        points=exercise.points,
        bucket_object_id=exercise.question.content.id,
        multiple_choice_id=exercise.question_type.content.id,
    )
