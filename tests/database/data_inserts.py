from datetime import UTC, datetime
from typing import Any, TypeAlias
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.models.media_types import MediaType

DbData: TypeAlias = dict[str, Any]
DbMixedData: TypeAlias = dict[str, dict[str, Any] | list[dict[str, Any]]]


def insert_assessment(session: Session, name: str = "") -> DbData:
    """Insert single assessment into database"""
    assessment = {
        "id": uuid4(),
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": name if name != "" else "Test Assessment"
    }
    session.execute(
        text(
            """
            INSERT INTO assessments(id, created_at, name)
            VALUES (:id, :created_at, :name)
            """
        ),
        assessment
    )
    return assessment


def connect_assessment_with_tasks(session: Session, assessment_id: UUID, task_ids: list[UUID]) -> None:
    """Connect a list of primers and exercises with an assessment"""
    for pos, task_id in enumerate(task_ids, start=1):
        session.execute(
            text(
                """
                INSERT INTO assessments_tasks(position, assessment_id, task_id)
                VALUES (:position, :assessment_id, :task_id)
                """
            ),
            {
                "position": pos,
                "assessment_id": assessment_id,
                "task_id": task_id
            }
        )


def insert_bucket_object(
        session: Session,
        media_type: MediaType = MediaType.VIDEO,
        bucket_name: None | str = None,
        filename: str = ""
) -> DbData:
    """Insert bucket_object object information (video file) into database"""
    bucket_object = {
        "id": uuid4(),
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket": bucket_name if bucket_name is not None else "testportal",
        "key": filename if filename else f"{uuid4()}.mpeg",
        "media_type": media_type.value
    }
    session.execute(
        text(
            """
            INSERT INTO bucket_objects(id, created_at, bucket, key, media_type)
            VALUES (:id, :created_at, :bucket, :key, :media_type)
            """
        ),
        bucket_object
    )
    return bucket_object


def insert_choice(session: Session, bucket_object_id: UUID) -> DbData:
    """Insert a choice (bucket_object, not text) to database"""
    choice = {
        "id": uuid4(),
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket_object_id": bucket_object_id,
    }
    session.execute(
        text(
            """
            INSERT INTO choices(id, created_at, bucket_object_id)
            VALUES (:id, :created_at, :bucket_object_id)
            """
        ),
        choice
    )
    return choice


def insert_exercise(session: Session, bucket_object_id: UUID, multiple_choice_id: UUID, points: int = 1) -> DbData:
    """Insert a multiple choice exercise into database"""
    task = insert_task(session, "exercise")

    exercise = {
        "points": points,
        "id": task.get("id"),
        "bucket_object_id": bucket_object_id,
        "multiple_choice_id": multiple_choice_id
    }
    session.execute(
        text(
            """
            INSERT INTO exercises(points, id, bucket_object_id, multiple_choice_id)
            VALUES (:points, :id, :bucket_object_id, :multiple_choice_id)
            """
        ),
        exercise
    )
    return exercise


def insert_multiple_choice(session: Session) -> DbData:
    """Insert a multiple choice into database"""
    multiple_choice = {
        "id": uuid4(),
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
    }
    session.execute(
        text(
            """
            INSERT INTO multiple_choices(id, created_at)
            VALUES (:id, :created_at)
            """
        ),
        multiple_choice
    )
    return multiple_choice


def connect_multiple_choice_with_choices(session: Session, multiple_choice_id: UUID, choice_ids: list[UUID]) -> None:
    """Connect a list of choices with a multiple choice"""
    for pos, choice_id in enumerate(choice_ids, start=1):
        session.execute(
            text(
                """
                INSERT INTO multiple_choices_choices(position, is_correct, choice_id, multiple_choice_id)
                VALUES (:position, :is_correct, :choice_id, :multiple_choice_id)
                """
            ),
            {
                "position": pos,
                "is_correct": pos == 1,
                "choice_id": choice_id,
                "multiple_choice_id": multiple_choice_id
            }
        )


def insert_primer(session: Session, bucket_object_id: UUID) -> DbData:
    """Insert a primer into database"""
    task = insert_task(session, "primer")
        
    primer = {
        "id": task.get("id"),
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket_object_id": bucket_object_id
    }
    session.execute(
        text(
            """
            INSERT INTO primers(id, bucket_object_id)
            VALUES (:id, :bucket_object_id)
            """
        ),
        primer
    )
    return primer


def insert_task(session: Session, task_type: str) -> DbData:
    """Insert a task into database"""
    task = {
        "id": uuid4(),
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "task_type": task_type,
    }
    session.execute(
        text(
            """
            INSERT INTO tasks(id, created_at, task_type)
            VALUES (:id, :created_at, :task_type);
            """
        ),
        task
    )
    return task


def insert_submission(session: Session, exercise_id: UUID, multiple_choice_id: UUID, choices: list[UUID]) -> DbData:
    """Insert a submission into database"""
    submission = {
        "id": uuid4(),
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "user_name": str(uuid4()),
        "choices": choices,
        "exercise_id": exercise_id,
        "multiple_choice_id": multiple_choice_id
    }
    session.execute(
        text(
            """
            INSERT INTO submissions(id, created_at, user_name, choices, exercise_id, multiple_choice_id)
            VALUES (:id, :created_at, :user_name, :choices, :exercise_id, :multiple_choice_id)
            """
        ),
        submission
    )
    return submission
