from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import text

from app.core.models.assessment import Assessment
from app.repositories.assessments import (
    add_assessment, delete_assessment_by_id, get_assessment_by_id, list_assessments, update_assessment
)


def test_add_assessment(db_session):
    assessment = Assessment(name="Test Assessment")
    add_assessment(db_session, assessment)

    result = db_session.execute(text("SELECT * FROM assessments")).fetchone()

    assert result[2] == "Test Assessment"


def test_get_assessment_by_id(db_session):
    _id = uuid4()
    date = datetime.now(timezone.utc)
    db_session.execute(
        text("INSERT INTO assessments(id, created_at, name) VALUES (:_id, :date, :name)"),
        {"_id": _id, "date": date, "name": "Test Assessment"}
    )

    result = get_assessment_by_id(session=db_session, _id=_id)

    assert result == Assessment(
        id=_id,
        created_at=date,
        name="Test Assessment",
        items=[]
    )


def test_list_no_assessments(db_session):
    result = list_assessments(db_session)
    assert result == []


def test_list_multiple_assessments(db_session):
    for i in range(100):
        db_session.execute(
            text("INSERT INTO assessments(name) VALUES (:name)"),
            {"name": f"Test Assessment {i}"}
        )

    result = list_assessments(db_session)

    assert len(result) == 100


def test_update_assessment(db_session):
    _id = db_session.execute(
        text("INSERT INTO assessments(name) VALUES (:name) RETURNING id"),
        {"name": "Test Assessment"}
    ).mappings().first()["id"]

    before_update = get_assessment_by_id(session=db_session, _id=_id)
    update_assessment(
        session=db_session,
        assessment=before_update,
        **{"name": "Updated Assessment"}
    )
    after_update = get_assessment_by_id(session=db_session, _id=_id)

    assert before_update.name == "Test Assessment"
    assert after_update.name == "Updated Assessment"
    assert len(list_assessments(db_session)) == 1


def test_delete_assessment(db_session):
    _id = db_session.execute(
        text("INSERT INTO assessments(name) VALUES (:name) RETURNING id"),
        {"name": "Test Assessment"}
    ).mappings().first()["id"]

    delete_assessment_by_id(session=db_session, _id=_id)
    result = get_assessment_by_id(session=db_session, _id=_id)

    assert result is None


def test_delete_one_of_two_assessments(db_session):
    _id = db_session.execute(
        text("INSERT INTO assessments(name) VALUES (:name) RETURNING id"),
        {"name": "Test Assessment 1"}
    ).mappings().first()["id"]
    db_session.execute(
        text("INSERT INTO assessments(name) VALUES (:name)"),
        {"name": "Test Assessment 2"}
    )

    before_deletion = list_assessments(db_session)
    delete_assessment_by_id(session=db_session, _id=_id)
    after_deletion = list_assessments(db_session)

    assert len(before_deletion) == 2
    assert len(after_deletion) == 1
    assert after_deletion[0].id != _id
