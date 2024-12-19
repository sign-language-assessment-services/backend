from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType
from app.database.tables.assessments import DbAssessment
from app.database.tables.assessments_tasks import assessments_tasks
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from database.data_inserts import (
    connect_assessment_with_tasks, insert_assessment, insert_bucket_object, insert_exercise, insert_multiple_choice,
    insert_primer, insert_task
)


def test_assessment_and_task_connection(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    primer_data = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))
    multiple_choice_data = insert_multiple_choice(session=db_session)
    exercise_1 = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )
    exercise_2 = insert_exercise(
        session=db_session,
        bucket_object_id=bucket_data.get("id"),
        multiple_choice_id=multiple_choice_data.get("id")
    )
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[primer_data.get("id"), exercise_1.get("id"), exercise_2.get("id")]
    )

    db_assessment = db_session.scalar(db_session.query(DbAssessment))
    association_table_counts = db_session.execute(
        select(func.count()).select_from(assessments_tasks)
    ).scalar_one()

    assert len(db_assessment.tasks) == 3
    assert association_table_counts == 3


def test_task_deletion_is_reflected_in_association_table(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    primer_data_1 = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))
    primer_data_2 = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))
    primer_data_3 = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[p.get("id") for p in (primer_data_1, primer_data_2, primer_data_3)]
    )

    db_primer_2 = db_session.scalar(select(DbPrimer).where(DbPrimer.id == primer_data_2.get("id")))
    db_session.delete(db_primer_2)
    db_session.flush()
    association_table_counts = db_session.execute(
        select(func.count()).select_from(assessments_tasks)
    ).scalar_one()

    assert db_session.query(DbPrimer).count() == 2
    assert db_session.query(DbAssessment).count() == 1
    db_assessment = db_session.scalar(select(DbAssessment))
    assert len(db_assessment.tasks) == 2
    assert db_assessment.tasks[0].id == primer_data_1.get("id")
    assert db_assessment.tasks[1].id == primer_data_3.get("id")
    assert association_table_counts == 2


def test_assessment_deletion_is_reflected_in_association_table(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    bucket_data = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    primer_data = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[primer_data.get("id")]
    )

    db_assessment = db_session.scalar(select(DbAssessment))
    db_session.delete(db_assessment)
    db_session.flush()
    association_table_counts = db_session.execute(
        select(func.count()).select_from(assessments_tasks)
    ).scalar_one()

    assert db_session.query(DbAssessment).count() == 0
    assert association_table_counts == 0
    assert db_session.query(DbPrimer).count() == 1
    assert db_session.query(DbTask).count() == 1


def test_assessment_deletion_does_not_delete_tasks(db_session: Session) -> None:
    assessment = insert_assessment(session=db_session)
    bucket = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    primer = insert_primer(session=db_session, bucket_object_id=bucket.get("id"))
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment.get("id"),
        task_ids=[primer.get("id")]
    )

    db_assessment = db_session.scalar(select(DbAssessment))
    db_session.delete(db_assessment)
    db_session.flush()
    association_table_counts = db_session.execute(
        select(func.count()).select_from(assessments_tasks)
    ).scalar_one()

    assert db_session.query(DbAssessment).count() == 0
    assert association_table_counts == 0
    assert db_session.query(DbPrimer).count() == 1


def test_task_deletion_does_not_delete_assessment(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    task_data = insert_task(session=db_session, task_type="task")
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[task_data.get("id")]
    )

    db_task = db_session.scalar(select(DbTask))
    db_session.delete(db_task)
    db_session.flush()
    association_table_counts = db_session.execute(
        select(func.count()).select_from(assessments_tasks)
    ).scalar_one()

    assert db_session.query(DbTask).count() == 0
    assert association_table_counts == 0
    assert db_session.query(DbAssessment).count() == 1


def test_tasks_having_the_correct_position(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    task_data_1 = insert_task(session=db_session, task_type="task")
    task_data_2 = insert_task(session=db_session, task_type="task")
    task_data_3 = insert_task(session=db_session, task_type="task")
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[t.get("id") for t in (task_data_1, task_data_2, task_data_3)]
    )

    db_association_table = db_session.query(assessments_tasks).order_by(assessments_tasks.c.position).all()

    assert db_association_table[0].task_id == task_data_1.get("id")
    assert db_association_table[0].position == 1
    assert db_association_table[1].task_id == task_data_2.get("id")
    assert db_association_table[1].position == 2
    assert db_association_table[2].task_id == task_data_3.get("id")
    assert db_association_table[2].position == 3


def test_tasks_still_have_the_correct_position_after_deletion_of_one_task(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    task_data_1 = insert_task(session=db_session, task_type="task")
    task_data_2 = insert_task(session=db_session, task_type="task")
    task_data_3 = insert_task(session=db_session, task_type="task")
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[t.get("id") for t in (task_data_1, task_data_2, task_data_3)]
    )
    db_task_2 = db_session.scalar(select(DbTask).where(DbTask.id == task_data_2.get("id")))
    db_session.delete(db_task_2)

    db_association_table = db_session.query(assessments_tasks).order_by(assessments_tasks.c.position).all()

    assert db_association_table[0].task_id == task_data_1.get("id")
    assert db_association_table[0].position == 1
    assert db_association_table[1].task_id == task_data_3.get("id")
    assert db_association_table[1].position == 3
