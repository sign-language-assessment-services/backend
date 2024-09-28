from datetime import UTC, datetime

from app.database.tables.assessments import DbAssessment
from app.database.tables.choices import DbChoice
from app.database.tables.multimedia_files import DbMultiMediaFile
from database.choices.test_add_choices import _add_choices_data
from database.dependencies import EXERCISE_ID, add_exercise, add_multimedia_file


def test_delete_choice(db_session):
    multimedia_file_id = "00000000-0000-0000-aaaa-000000000000"
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "is_correct": True,
        "exercise_id": EXERCISE_ID,
        "multimedia_file_id": multimedia_file_id
    }
    add_exercise(db_session, with_dependencies=True)
    add_multimedia_file(db_session, _id=multimedia_file_id)
    _add_choices_data(db_session, **data)

    db_session.query(DbChoice).delete()

    assert db_session.query(DbChoice).count() == 0
    assert db_session.query(DbAssessment).count() == 1
    assert db_session.query(DbMultiMediaFile).count() == 2
