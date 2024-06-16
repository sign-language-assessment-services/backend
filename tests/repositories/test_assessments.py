from datetime import datetime, timezone

import pytest
from sqlalchemy import text

from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.primer import Primer
from app.repositories.assessments import (add_assessment, add_assessment_primer,
                                          delete_assessment_by_id, get_assessment_by_id,
                                          list_assessments)


def test_add_assessment(db_session):
    assessment = Assessment(name="Test Assessment")
    add_assessment(db_session, assessment)

    db_assessment = db_session.execute(text("SELECT * FROM assessments")).fetchone()

    assert db_assessment[2] == "Test Assessment"

    primer = Primer(
        position=1,
        assessment_id=assessment.id,
        multimedia_file_id=None,
    )
    add_assessment_primer(db_session, primer)

    db_primer = db_session.execute(text("SELECT * FROM primers")).fetchone()

    assert db_primer[2] == 1
    assert db_primer[3] == db_assessment[0]


def test_get_assessment_by_id(db_session, insert_assessments):
    insert_assessments(1)
    assert get_assessment_by_id(db_session, "test_id-1") == Assessment(
        id='test_id-1',
        created_at=datetime(2000, 12, 31, 12, 0, 1, tzinfo=timezone.utc),
        name='Test Assessment 1',
        items=[]
    )


def test_list_no_assessments(db_session):
    result = list_assessments(db_session)
    assert result == []


def test_list_one_assessment(db_session, insert_assessments):
    insert_assessments(1)

    result = list_assessments(db_session)

    assert result == [
        AssessmentSummary(
            name="Test Assessment 1",
            id="test_id-1"
        )
    ]


def test_list_multiple_assessments(db_session, insert_assessments):
    insert_assessments(100)

    result = list_assessments(db_session)

    assert len(result) == 100


def test_delete_one_of_two_assessments(db_session, insert_assessments):
    insert_assessments(2)

    delete_assessment_by_id(db_session, "test_id-1")

    assert get_assessment_by_id(db_session, "test_id-2")
    with pytest.raises(AttributeError):
        get_assessment_by_id(db_session, "test_id-1")
