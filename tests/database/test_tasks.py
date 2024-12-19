from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.database.tables.exercises import DbExercise
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from database.data_inserts import insert_task
from database.utils import table_count


def test_insert_task(db_session: Session) -> None:
    task_data = insert_task(session=db_session, task_type="task")

    db_task = db_session.get(DbTask, task_data.get("id"))
    assert table_count(db_session, DbTask) == 1
    assert db_task.id == task_data.get("id")
    assert db_task.created_at == task_data.get("created_at")
    assert db_task.task_type == task_data.get("task_type")


def test_update_task(db_session: Session) -> None:
    task_data = insert_task(session=db_session, task_type="task")

    db_session.execute(update(DbTask).values(created_at=datetime(1970, 1, 1, 0, tzinfo=UTC)))

    db_task = db_session.get(DbTask, task_data.get("id"))
    assert table_count(db_session, DbTask) == 1
    assert db_task.id == task_data.get("id")
    assert db_task.task_type == task_data.get("task_type")
    assert db_task.created_at != task_data.get("created_at")
    assert db_task.created_at == datetime(1970, 1, 1, 0, tzinfo=UTC)


def test_delete_task(db_session: Session) -> None:
    insert_task(session=db_session, task_type="task")

    db_task = db_session.scalar(select(DbTask))
    db_session.delete(db_task)

    assert table_count(db_session, DbTask) == 0
    assert table_count(db_session, DbPrimer) == 0
    assert table_count(db_session, DbExercise) == 0
