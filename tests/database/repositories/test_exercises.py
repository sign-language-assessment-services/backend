from sqlalchemy.orm import Session

from app.core.models.choice import Choice
from app.core.models.exercise import Exercise
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.question import Question
from app.core.models.question_type import QuestionType
from app.database.tables.exercises import DbExercise
from app.database.tables.tasks import DbTask
from app.repositories.exercises import add_exercise, delete_exercise, get_exercise, list_exercises, update_exercise
from tests.database.data_inserts import insert_bucket_object, insert_choice, insert_exercise, insert_multiple_choice
from tests.database.utils import table_count


def test_add_exercise(db_session: Session) -> None:
    question_video_id = insert_bucket_object(db_session).get("id")
    choice_video_id = insert_bucket_object(db_session).get("id")
    choice_id = insert_choice(db_session, choice_video_id).get("id")
    multiple_choice_id = insert_multiple_choice(db_session).get("id")
    exercise = Exercise(
        points=1,
        question=Question(
            content=MultimediaFile(
                id=question_video_id,
                location=MinioLocation(bucket="1", key="question"),
                media_type=MediaType.VIDEO
            )
        ),
        question_type=QuestionType(
            content=MultipleChoice(
                id=multiple_choice_id,
                choices=[
                    Choice(
                        id=choice_id,
                        content=MultimediaFile(
                            id=choice_video_id,
                            location=MinioLocation(bucket="1", key="choice"),
                            media_type=MediaType.VIDEO
                        )
                    )
                ]
            )
        )
    )

    add_exercise(db_session, exercise)

    result = db_session.get(DbExercise, exercise.id)
    assert result.id == exercise.id
    assert result.points == exercise.points
    assert result.bucket_object_id == exercise.question.content.id
    assert result.multiple_choice_id == exercise.question_type.content.id
    assert table_count(db_session, DbExercise) == 1
    assert table_count(db_session, DbTask) == 1


def test_get_exercise_by_id(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    mc_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, mc_id).get("id")

    result = get_exercise(db_session, exercise_id)

    assert result.id == exercise_id
    assert result.points == 1
    assert result.question.content.id == video_id
    assert result.question_type.content.id == mc_id
    assert table_count(db_session, DbExercise) == 1
    assert table_count(db_session, DbTask) == 1


def test_list_no_exercises(db_session: Session) -> None:
    result = list_exercises(db_session)

    assert result == []
    assert table_count(db_session, DbExercise) == 0
    assert table_count(db_session, DbTask) == 0


def test_list_multiple_exercises(db_session: Session) -> None:
    for i in range(100):
        video_id = insert_bucket_object(db_session).get("id")
        mc_id = insert_multiple_choice(db_session).get("id")
        insert_exercise(db_session, video_id, mc_id).get("id")

    result = list_exercises(db_session)

    assert len(result) == 100
    assert table_count(db_session, DbExercise) == 100
    assert table_count(db_session, DbTask) == 100


def test_update_exercise(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    mc_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, mc_id).get("id")

    updated_points = 2
    update_exercise(db_session, exercise_id, **{"points": updated_points})

    result = db_session.get(DbExercise, exercise_id)
    assert result.points == updated_points
    assert table_count(db_session, DbExercise) == 1
    assert table_count(db_session, DbTask) == 1


def test_delete_exercise(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    mc_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, mc_id).get("id")

    delete_exercise(db_session, exercise_id)

    result = db_session.get(DbExercise, exercise_id)
    assert result is None
    assert table_count(db_session, DbExercise) == 0
    assert table_count(db_session, DbTask) == 0


def test_delete_one_of_two_exercises(db_session: Session) -> None:
    video_id = insert_bucket_object(db_session).get("id")
    mc_id = insert_multiple_choice(db_session).get("id")
    exercise_id = insert_exercise(db_session, video_id, mc_id).get("id")
    insert_exercise(db_session, video_id, mc_id).get("id")

    delete_exercise(db_session, exercise_id)

    result = db_session.get(DbExercise, exercise_id)
    assert result is None
    assert table_count(db_session, DbExercise) == 1
    assert table_count(db_session, DbTask) == 1
