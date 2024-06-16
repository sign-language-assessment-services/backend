from datetime import datetime, timedelta
from typing import Callable

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session


@pytest.fixture
def insert_assessments(db_session: Session) -> Callable:
    def generate_assessments(number):
        for n in range(1, number + 1):
            statement = text(
                """
                INSERT INTO assessments(id, created_at, name)
                VALUES (:id, :created_at, :name)
                """
            )
            db_session.execute(
                statement, {
                    "id": f"test_id-{n}",
                    "created_at": datetime(2000, 12, 31, 12) + timedelta(seconds=n),
                    "name": f"Test Assessment {n}"
                }
            )

    yield generate_assessments

    db_session.execute(text("TRUNCATE assessments CASCADE"))


@pytest.fixture
def insert_multimedia_file(db_session) -> Callable:
    def generate_multimedia_files(number):
        for n in range(1, number + 1):
            statement = text(
                """
                INSERT INTO multimedia_files(id, created_at, bucket, key)
                VALUES (:id, :created_at, :bucket, :key)
                """
            )
            db_session.execute(
                statement, {
                    "id": f"test_id-{n}",
                    "created_at": datetime(2000, 12, 31, 12) + timedelta(seconds=n),
                    "bucket": "testportal",
                    "key": f"{n:03d}"
                }
            )

    yield generate_multimedia_files

    db_session.execute(text("TRUNCATE multimedia_files CASCADE"))


@pytest.fixture(scope="function")
def insert_submissions(insert_assessments, db_session) -> Callable:
    insert_assessments(1)

    def generate_submissions(number):
        for n in range(1, number + 1):
            statement = text(
                """
                INSERT INTO submissions(id, created_at, user_id, points, maximum_points, percentage, assessment_id)
                VALUES (:id, :created_at, :user_id, :points, :maximum_points, :percentage, :assessment_id)
                """
            )
            db_session.execute(
                statement, {
                    "id": f"test_id-{n}",
                    "created_at": datetime(2000, 12, 31, 12) + timedelta(seconds=n),
                    "user_id": "test_user_id",
                    "points": 1,
                    "maximum_points": 1,
                    "percentage": 100.0,
                    "assessment_id": "test_id-1"
                }
            )

    yield generate_submissions

    db_session.execute(text("TRUNCATE submissions CASCADE"))
