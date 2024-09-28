from datetime import UTC, datetime

from app.database.tables.assessments import DbAssessment
from app.database.tables.multimedia_files import DbMultiMediaFile
from app.database.tables.primers import DbPrimer
from database.exercises.test_add_exercises import (
    _add_exercise_data
)
from database.dependencies import add_assessment, add_multimedia_file


def test_delete_exercises(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "position": 1,
        "assessment_id": "00000000-0000-0000-0000-000000000000",
        "multimedia_file_id": "00000000-0000-0000-0000-000000000001"
    }
    add_assessment(db_session)
    add_multimedia_file(db_session)
    _add_exercise_data(db_session, **data)

    db_session.query(DbPrimer).delete()

    assert db_session.query(DbPrimer).count() == 0
    assert db_session.query(DbAssessment).count() == 1
    assert db_session.query(DbMultiMediaFile).count() == 1
