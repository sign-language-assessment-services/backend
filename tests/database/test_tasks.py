from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.database.tables.exercises import DbExercise
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from database.data_inserts import insert_task


def test_insert_task(db_session: Session) -> None:
    task_data = insert_task(session=db_session, task_type="task")

    data_query = db_session.query(DbTask)

    assert data_query.count() == 1
    db_task = data_query.first()
    assert db_task.id == task_data.get("id")
    assert db_task.created_at == task_data.get("created_at")
    assert db_task.task_type == task_data.get("task_type")


def test_update_task(db_session: Session) -> None:
    task_data = insert_task(session=db_session, task_type="task")

    db_session.query(DbTask).update({"created_at": datetime(1970, 1, 1, 0, tzinfo=UTC)})

    data_query = db_session.query(DbTask)
    assert data_query.count() == 1
    db_task = data_query.first()
    assert db_task.id == task_data.get("id")
    assert db_task.task_type == task_data.get("task_type")
    assert db_task.created_at != task_data.get("created_at")
    assert db_task.created_at == datetime(1970, 1, 1, 0, tzinfo=UTC)


def test_delete_task(db_session: Session) -> None:
    insert_task(session=db_session, task_type="task")

    db_session.query(DbTask).delete()

    assert db_session.query(DbTask).count() == 0
    assert db_session.query(DbPrimer).count() == 0
    assert db_session.query(DbExercise).count() == 0
