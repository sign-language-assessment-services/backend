from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer
from app.database.tables.exercises import DbExercise
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from app.repositories.tasks import get_task
from tests.database.data_inserts import (
    insert_bucket_object, insert_exercise, insert_multiple_choice, insert_primer
)
from tests.database.utils import table_count


def test_get_task_by_id_returns_primer(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    primer = insert_primer(session=db_session, bucket_object_id=video_id)

    result = get_task(session=db_session, _id=primer.get("id"))

    assert isinstance(result, Primer)
    assert result.id == primer.get("id")
    assert result.content.id == video_id
    assert table_count(db_session, DbPrimer) == 1
    assert table_count(db_session, DbTask) == 1
    assert table_count(db_session, DbExercise) == 0


def test_get_task_by_id_returns_exercise(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    multiple_choice_id = insert_multiple_choice(session=db_session).get("id")
    exercise = insert_exercise(
        session=db_session,
        bucket_object_id=video_id,
        multiple_choice_id=multiple_choice_id
    )

    result = get_task(session=db_session, _id=exercise.get("id"))

    assert isinstance(result, Exercise)
    assert result.id == exercise.get("id")
    assert result.question.content.id == video_id
    assert table_count(db_session, DbExercise) == 1
    assert table_count(db_session, DbTask) == 1
    assert table_count(db_session, DbPrimer) == 0


def test_get_task_by_id_returns_none_if_not_found(db_session: Session) -> None:
    result = get_task(session=db_session, _id=uuid4())

    assert result is None
