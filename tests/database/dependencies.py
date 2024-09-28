from datetime import UTC, datetime

from sqlalchemy import text


def add_assessment(session) -> None:
    assessment = {
        "id": "00000000-0000-0000-0000-000000000000",
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


def add_multimedia_file(session) -> None:
    multimedia_file = {
        "id": "00000000-0000-0000-0000-000000000001",
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
