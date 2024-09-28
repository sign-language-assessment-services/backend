from datetime import UTC, datetime

from app.database.tables.assessments import DbAssessment
from database.assessments.test_add_assessments import _add_assessment_data


def test_delete_assessment(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Test Assessment"
    }

    _add_assessment_data(db_session, **data)

    db_session.query(DbAssessment).delete()
    assert db_session.query(DbAssessment).count() == 0
