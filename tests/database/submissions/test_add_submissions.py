import re
from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.database.tables.submissions import DbSubmission
from database.dependencies import ASSESSMENT_ID, add_assessment


def test_insert_valid_submission(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "user_id": "access_key_from_minio",
        "points": 20,
        "maximum_points": 100,
        "percentage": 20,
        "assessment_id": ASSESSMENT_ID
    }

    add_assessment(db_session)
    _add_submission_data(db_session, **data)

    data_query = db_session.query(DbSubmission)
    assert data_query.count() == 1
    assert data_query.first().id == UUID(data.get("id"))
    assert data_query.first().created_at == data.get("created_at")
    assert data_query.first().user_id == data.get("user_id")
    assert data_query.first().points == data.get("points")
    assert data_query.first().maximum_points == data.get("maximum_points")
    assert data_query.first().percentage == data.get("percentage")
    assert isinstance(data_query.first().percentage, float)
    assert data_query.first().assessment_id == UUID(data.get("assessment_id"))


def test_insert_submission_with_missing_assessment_fails(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "user_id": "access_key_from_minio",
        "points": 20,
        "maximum_points": 100,
        "percentage": 20/100,
        "assessment_id": ASSESSMENT_ID
    }

    failure_details = re.compile(
        r'violates foreign key constraint.*not present in table "assessments"',
        re.DOTALL
    )
    with pytest.raises(IntegrityError, match=failure_details):
        _add_submission_data(db_session, **data)


def _add_submission_data(session, **kwargs) -> None:
    statement = text(
        """
        INSERT INTO Submissions(id, created_at, user_id, points, maximum_points, percentage, assessment_id)
        VALUES (:id, :created_at, :user_id, :points, :maximum_points, :percentage, :assessment_id)
        """
    )
    session.execute(statement, kwargs)
