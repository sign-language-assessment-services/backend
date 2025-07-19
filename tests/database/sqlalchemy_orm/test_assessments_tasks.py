from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.tables.assessments import DbAssessment
from app.database.tables.assessments_tasks import DbAssessmentsTasks
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from tests.database.data_inserts import (
    connect_assessment_with_tasks, insert_assessment, insert_bucket_object, insert_exercise,
    insert_multiple_choice, insert_primer, insert_task
)
from tests.database.utils import table_count


def test_assessment_and_task_connection(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    bucket_data = insert_bucket_object(session=db_session)
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

    db_assessment = db_session.execute(select(DbAssessment)).scalar_one()
    assert table_count(db_session, DbAssessmentsTasks) == 3
    assert len(db_assessment.tasks) == 3
    assert db_assessment.tasks[0].task_type == "primer"
    assert db_assessment.tasks[1].task_type == "exercise"
    assert db_assessment.tasks[2].task_type == "exercise"


def test_task_deletion_is_reflected_in_association_table(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    bucket_data = insert_bucket_object(session=db_session)
    primer_data_1 = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))
    primer_data_2 = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))
    primer_data_3 = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[p.get("id") for p in (primer_data_1, primer_data_2, primer_data_3)]
    )

    db_primer_2 = db_session.get(DbPrimer, primer_data_2.get("id"))
    db_session.delete(db_primer_2)
    db_session.flush()

    db_assessment = db_session.execute(select(DbAssessment)).scalar_one()
    assert table_count(db_session, DbAssessment) == 1
    assert table_count(db_session, DbPrimer) == 2
    assert table_count(db_session, DbAssessmentsTasks) == 2
    assert len(db_assessment.tasks) == 2
    assert db_assessment.tasks[0].id == primer_data_1.get("id")
    assert db_assessment.tasks[1].id == primer_data_3.get("id")


def test_assessment_deletion_is_reflected_in_association_table(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    bucket_data = insert_bucket_object(session=db_session)
    primer_data = insert_primer(session=db_session, bucket_object_id=bucket_data.get("id"))
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[primer_data.get("id")]
    )

    db_assessment = db_session.get(DbAssessment, assessment_data.get("id"))
    db_session.delete(db_assessment)

    assert table_count(db_session, DbAssessment) == 0
    assert table_count(db_session, DbAssessmentsTasks) == 0
    assert table_count(db_session, DbPrimer) == 1
    assert table_count(db_session, DbTask) == 1


def test_assessment_deletion_does_not_delete_tasks(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    bucket_object_data = insert_bucket_object(session=db_session)
    primer_data = insert_primer(session=db_session, bucket_object_id=bucket_object_data.get("id"))
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[primer_data.get("id")]
    )

    db_assessment = db_session.get(DbAssessment, assessment_data.get("id"))
    db_session.delete(db_assessment)

    assert table_count(db_session, DbAssessment) == 0
    assert table_count(db_session, DbAssessmentsTasks) == 0
    assert table_count(db_session, DbPrimer) == 1


def test_task_deletion_does_not_delete_assessment(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    task_data = insert_task(session=db_session, task_type="task")
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[task_data.get("id")]
    )

    db_task = db_session.get(DbTask, task_data.get("id"))
    db_session.delete(db_task)
    db_session.flush()

    assert table_count(db_session, DbTask) == 0
    assert table_count(db_session, DbAssessmentsTasks) == 0
    assert table_count(db_session, DbAssessment) == 1


def test_tasks_having_the_correct_position(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    tasks = {
        1: insert_task(session=db_session, task_type="task"),
        2: insert_task(session=db_session, task_type="task"),
        3: insert_task(session=db_session, task_type="task")
    }

    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[task.get("id") for _, task in sorted(tasks.items())]
    )

    db_associations = db_session.execute(select(DbAssessmentsTasks).order_by(DbAssessmentsTasks.position)).scalars()
    for pos, db_association in enumerate(db_associations, start=1):
        assert db_association.task_id == tasks[pos].get("id")
        assert db_association.position == pos


def test_tasks_still_have_the_correct_position_after_deletion_of_one_task(db_session: Session) -> None:
    assessment_data = insert_assessment(session=db_session)
    tasks = {
        1: insert_task(session=db_session, task_type="task"),
        2: insert_task(session=db_session, task_type="task"),
        3: insert_task(session=db_session, task_type="task")
    }
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment_data.get("id"),
        task_ids=[task.get("id") for _, task in sorted(tasks.items())]
    )

    db_task_2 = db_session.get(DbTask, tasks[2].get("id"))
    db_session.delete(db_task_2)
    db_session.flush()

    db_associations = db_session.execute(
        select(DbAssessmentsTasks).order_by(DbAssessmentsTasks.position)
    ).scalars().all()
    assert db_associations[0].task_id == tasks[1].get("id")
    assert db_associations[0].position == 1
    assert db_associations[1].task_id == tasks[3].get("id")
    assert db_associations[1].position == 3
