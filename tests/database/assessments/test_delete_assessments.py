from datetime import UTC, datetime

from app.database.tables.assessments import DbAssessment
from app.database.tables.exercises import DbExercise
from app.database.tables.multimedia_files import DbMultiMediaFile
from app.database.tables.primers import DbPrimer
from app.database.tables.submissions import DbSubmission
from database.assessments.test_add_assessments import _add_assessment_data
from database.dependencies import add_exercise, add_primer, add_submission


def test_delete_assessment(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Test Assessment"
    }
    _add_assessment_data(db_session, **data)

    db_session.query(DbAssessment).delete()

    assert db_session.query(DbAssessment).count() == 0


def test_delete_assessment_also_deletes_exercise(db_session):
    add_exercise(db_session)

    db_session.query(DbAssessment).delete()

    assert db_session.query(DbAssessment).count() == 0
    assert db_session.query(DbExercise).count() == 0


def test_delete_assessment_with_exercise_does_not_delete_multimedia_file(db_session):
    add_exercise(db_session)

    db_session.query(DbAssessment).delete()

    assert db_session.query(DbMultiMediaFile).count() == 1


def test_delete_assessment_also_deletes_primer(db_session):
    add_primer(db_session)

    db_session.query(DbAssessment).delete()

    assert db_session.query(DbAssessment).count() == 0
    assert db_session.query(DbPrimer).count() == 0


def test_delete_assessment_with_primer_does_not_delete_multimedia_file(db_session):
    add_primer(db_session)

    db_session.query(DbAssessment).delete()

    assert db_session.query(DbMultiMediaFile).count() == 1


def test_delete_assessment_also_deletes_submission(db_session):
    add_submission(db_session)

    db_session.query(DbAssessment).delete()

    assert db_session.query(DbAssessment).count() == 0
    assert db_session.query(DbSubmission).count() == 0
