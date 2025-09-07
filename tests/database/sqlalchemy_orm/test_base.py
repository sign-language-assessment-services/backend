from datetime import UTC, datetime, timezone
from uuid import UUID, uuid4

import pytest
import pytz
from sqlalchemy import select, text
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

from app.database.tables.assessments import DbAssessment
from app.database.tables.base import DbBase


def test_insert_assessment_with_wrong_uuid(db_session: Session) -> None:
    data = {
        "id": "this_isn-t_av-alid-uuid-is_not_good.",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Test Assessment"
    }

    with pytest.raises(DataError, match=r"invalid input syntax for type uuid"):
        _add_assessment_data(db_session, **data)


def test_insert_two_assessments_with_same_id_will_fail(db_session: Session) -> None:
    any_uuid = uuid4()
    data_1 = {
        "id": any_uuid,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Foo"
    }
    _add_assessment_data(db_session, **data_1)

    with pytest.raises(IntegrityError, match=r"duplicate key value violates unique constraint"):
        data_2 = {
            "id": any_uuid,
            "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
            "name": "Bar"
        }
        _add_assessment_data(db_session, **data_2)


def test_insert_assessment_with_wrong_date(db_session: Session) -> None:
    data = {
        "id": uuid4(),
        "created_at": "2000-1-1 25:00",
        "name": "Test Assessment"
    }

    with pytest.raises(DataError, match=r"date/time field value out of range"):
        _add_assessment_data(db_session, **data)


def test_insert_assessment_without_timezone_returns_utc(db_session: Session) -> None:
    data = {
        "id": uuid4(),
        "created_at": datetime(2000, 1, 1, 12),
        "name": "Test Assessment"
    }

    _add_assessment_data(db_session, **data)

    db_assessment = db_session.scalars(select(DbAssessment).limit(1)).first()
    assert db_assessment.created_at == datetime(2000, 1, 1, 12, tzinfo=UTC)


def test_insert_assessment_with_different_timezone_saves_it_as_utc(db_session: Session) -> None:
    berlin_time = pytz.timezone("Europe/Berlin").localize(datetime(2000, 1, 1, 12))
    data = {
        "id": uuid4(),
        "created_at": berlin_time,
        "name": "Test Assessment"
    }

    _add_assessment_data(db_session, **data)

    db_assessment = db_session.scalars(select(DbAssessment).limit(1)).first()
    assert db_assessment.created_at == berlin_time
    assert db_assessment.created_at.tzinfo == timezone.utc
    assert db_assessment.created_at == datetime(2000, 1, 1, 11, tzinfo=UTC)


def test_repr_of_base_class() -> None:
    base = DbBase(
        id=uuid4(),
        created_at=datetime(2000, 1, 1, 12, tzinfo=UTC),
    )

    expected = (
        f"<{base.__class__.__name__}[{id(base)}] "
        f"(id={base.id!r}, created_at={base.created_at!r})>"
    )
    assert repr(base) == expected
    assert str(base) == expected


def _add_assessment_data(session: Session, **kwargs: dict[str, UUID | datetime | str]) -> None:
    statement = text(
        """
        INSERT INTO assessments(id, created_at, name)
        VALUES (:id, :created_at, :name)
        """
    )
    session.execute(statement, kwargs)
