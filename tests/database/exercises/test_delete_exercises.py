from datetime import UTC, datetime

from app.database.tables.assessments import DbAssessment
from app.database.tables.choices import DbChoice
from app.database.tables.exercises import DbExercise
from app.database.tables.multimedia_files import DbMultiMediaFile
from app.database.tables.primers import DbPrimer
from database.exercises.test_add_exercises import (
    _add_exercise_data
)
from database.dependencies import (
    ASSESSMENT_ID, MULTIMEDIA_FILE_ID, add_assessment, add_exercise, add_multimedia_file,
    add_choice
)


def test_delete_exercises(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "position": 1,
        "assessment_id": ASSESSMENT_ID,
        "multimedia_file_id": MULTIMEDIA_FILE_ID
    }
    add_assessment(db_session)
    add_multimedia_file(db_session)
    _add_exercise_data(db_session, **data)

    db_session.query(DbPrimer).delete()

    assert db_session.query(DbPrimer).count() == 0
    assert db_session.query(DbAssessment).count() == 1
    assert db_session.query(DbMultiMediaFile).count() == 1


def test_delete_exercise_does_not_delete_multimedia_file(db_session):
    add_exercise(db_session)

    db_session.query(DbExercise).delete()

    assert db_session.query(DbMultiMediaFile).count() == 1


def test_delete_exercise_also_deletes_choice(db_session):
    add_choice(db_session)

    db_session.query(DbExercise).delete()

    assert db_session.query(DbExercise).count() == 0
    assert db_session.query(DbChoice).count() == 0


def test_delete_exercise_with_choice_does_not_delete_multimedia_file(db_session):
    add_choice(db_session)

    db_session.query(DbExercise).delete()

    assert db_session.query(DbMultiMediaFile).count() == 2
