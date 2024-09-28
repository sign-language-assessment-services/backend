from datetime import UTC, datetime

from sqlalchemy import text


ASSESSMENT_ID = "00000000-0000-0000-0000-000000000000"
MULTIMEDIA_FILE_ID = "00000000-0000-0000-0000-000000000001"
EXERCISE_ID = "00000000-0000-0000-0000-000000000002"


def add_assessment(session) -> None:
    assessment = {
        "id": ASSESSMENT_ID,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Test Assessment"
    }
    assessment_statement = text(
        """
        INSERT INTO assessments(id, created_at, name)
        VALUES (:id, :created_at, :name)
        """
    )
    session.execute(assessment_statement, assessment)


def add_multimedia_file(session, _id: str | None = None) -> None:
    multimedia_file = {
        "id": MULTIMEDIA_FILE_ID if _id is None else _id,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket": "testportal",
        "key": "test.mpeg",
        "mediatype": "VIDEO"
    }
    multimedia_file_statement = text(
        """
        INSERT INTO multimedia_files(id, created_at, bucket, key, mediatype)
        VALUES (:id, :created_at, :bucket, :key, :mediatype)
        """
    )
    session.execute(multimedia_file_statement, multimedia_file)


def add_exercise(session, with_dependencies=True) -> None:
    if with_dependencies:
        add_assessment(session)
        add_multimedia_file(session)

    exercise = {
        "id": EXERCISE_ID,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "position": 1,
        "assessment_id": ASSESSMENT_ID,
        "multimedia_file_id": MULTIMEDIA_FILE_ID
    }
    exercise_statement = text(
        """
        INSERT INTO exercises(id, created_at, position, assessment_id, multimedia_file_id)
        VALUES (:id, :created_at, :position, :assessment_id, :multimedia_file_id)
        """
    )
    session.execute(exercise_statement, exercise)
