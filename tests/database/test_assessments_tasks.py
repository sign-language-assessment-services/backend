from sqlalchemy import func, select

from app.core.models.media_types import MediaType
from app.database.tables.assessments import DbAssessment
from app.database.tables.assessments_tasks import assessments_tasks
from app.database.tables.primers import DbPrimer
from database.data_inserts import (
    connect_assessment_with_tasks, insert_assessment, insert_bucket_object, insert_exercise, insert_multiple_choice,
    insert_primer
)


def test_assessment_and_task_connection(db_session) -> None:
    assessment = insert_assessment(session=db_session)
    bucket = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    primer = insert_primer(session=db_session, bucket_object_id=bucket.get("id"))
    multiple_choice = insert_multiple_choice(session=db_session)
    exercise_1 = insert_exercise(
        session=db_session,
        bucket_object_id=bucket.get("id"),
        multiple_choice_id=multiple_choice.get("id")
    )
    exercise_2 = insert_exercise(
        session=db_session,
        bucket_object_id=bucket.get("id"),
        multiple_choice_id=multiple_choice.get("id")
    )
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment.get("id"),
        task_ids=[primer.get("id"), exercise_1.get("id"), exercise_2.get("id")]
    )

    db_assessment = db_session.scalar(db_session.query(DbAssessment))
    association_table_counts = db_session.execute(
        select(func.count()).select_from(assessments_tasks)
    ).scalar_one()

    assert len(db_assessment.tasks) == 3
    assert association_table_counts == 3


def test_task_deletion_is_reflected_in_assessment_tasks(db_session) -> None:
    assessment = insert_assessment(session=db_session)
    bucket = insert_bucket_object(session=db_session, content_type=MediaType.VIDEO)
    primer_1 = insert_primer(session=db_session, bucket_object_id=bucket.get("id"))
    primer_2 = insert_primer(session=db_session, bucket_object_id=bucket.get("id"))
    primer_3 = insert_primer(session=db_session, bucket_object_id=bucket.get("id"))
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment.get("id"),
        task_ids=[primer_1.get("id"), primer_2.get("id"), primer_3.get("id")]
    )

    db_primer_2 = db_session.scalar(select(DbPrimer).where(DbPrimer.id == primer_2.get("id")))
    db_session.delete(db_primer_2)
    db_session.flush()
    association_table_counts = db_session.execute(
        select(func.count()).select_from(assessments_tasks)
    ).scalar_one()

    assert db_session.query(DbPrimer).count() == 2
    assert db_session.query(DbAssessment).count() == 1  # assessment is not deleted
    db_assessment = db_session.scalar(select(DbAssessment))
    assert len(db_assessment.tasks) == 2
    assert db_assessment.tasks[0].id == primer_1.get("id")
    assert db_assessment.tasks[1].id == primer_3.get("id")
    assert association_table_counts == 2


def test_assessment_deletion_does_not_delete_tasks(db_session) -> None:
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
    assert db_session.query(DbPrimer).count() == 1
    assert association_table_counts == 0
