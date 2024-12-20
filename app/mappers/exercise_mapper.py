from app.core.models.exercise import Exercise
from app.database.tables.exercises import DbExercise
from app.mappers.multimedia_file_mapper import bucket_object_to_domain
from app.mappers.multiple_choice_mapper import multiple_choice_to_domain
from app.mappers.submission_mapper import submission_to_db, submission_to_domain


def exercise_to_domain(db_exercise: DbExercise) -> Exercise:
    return Exercise(
        id=db_exercise.id,
        created_at=db_exercise.created_at,
        points=db_exercise.points,
        question=bucket_object_to_domain(db_exercise.bucket_object),
        question_type=multiple_choice_to_domain(db_exercise.multiple_choice),
        submissions=[submission_to_domain(s) for s in db_exercise.submissions]
    )


def exercise_to_db(exercise: Exercise) -> DbExercise:
    return DbExercise(
        id=exercise.id,
        created_at=exercise.created_at,
        points=exercise.points,
        bucket_object_id=exercise.question.id,
        multiple_choice_id=exercise.question_type.id,
        submissions=[submission_to_db(s) for s in exercise.submissions]
    )
