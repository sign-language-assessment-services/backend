from datetime import UTC, datetime

from app.database.tables.assessments import DbAssessment
from app.database.tables.submissions import DbSubmission
from database.dependencies import ASSESSMENT_ID, add_assessment
from database.submissions.test_add_submissions import _add_submission_data


def test_delete_submissions(db_session):
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

    db_session.query(DbSubmission).delete()

    assert db_session.query(DbSubmission).count() == 0
    assert db_session.query(DbAssessment).count() == 1
