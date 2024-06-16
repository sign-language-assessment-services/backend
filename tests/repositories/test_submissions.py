import math
import uuid
from datetime import datetime, timezone
from typing import Callable

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.core.models.submission import Submission
from app.repositories.assessments import add_assessment
from app.repositories.submissions import (add_submission, delete_submission_by_id,
                                          get_submission_by_id, list_submissions)


def test_add_submission(db_session: Session) -> None:
    assessment = Assessment(name="Test Assessment")
    add_assessment(db_session, assessment)
    submission = Submission(
        user_id=str(uuid.uuid4()),
        assessment_id=assessment.id,
        answers={1: [0], 2: [1]},
        points=2,
        maximum_points=3,
        percentage=100.0
    )
    add_submission(db_session, submission)

    db_submission = db_session.execute(text("SELECT * FROM submissions")).fetchone()

    assert db_submission[3] == 2
    assert db_submission[4] == 3
    assert math.isclose(db_submission[5], 100.0)
    assert db_submission[6] == assessment.id


def test_get_submission_by_id(db_session: Session, insert_submissions: Callable) -> None:
    insert_submissions(1)
    assert get_submission_by_id(db_session, _id="test_id-1") == Submission(
        id="test_id-1",
        created_at=datetime(2000, 12, 31, 12, 0, 1, tzinfo=timezone.utc),
        user_id="test_user_id",
        points=1,
        maximum_points=1,
        percentage=100.0,
        assessment_id="test_id-1",
        answers=[]
    )


def test_list_no_submissions(db_session: Session) -> None:
    result = list_submissions(db_session)
    assert result == []


def test_list_one_submission(db_session: Session, insert_submissions: Callable) -> None:
    insert_submissions(1)

    result = list_submissions(db_session)

    assert result == [
        Submission(
            id='test_id-1',
            created_at=datetime(2000, 12, 31, 12, 0, 1, tzinfo=timezone.utc),
            user_id='test_user_id',
            points=1,
            maximum_points=1,
            percentage=100.0,
            assessment_id='test_id-1',
            answers=[]
        )
    ]


def test_list_multiple_submissions(db_session: Session, insert_submissions: Callable) -> None:
    insert_submissions(100)

    result = list_submissions(db_session)

    assert len(result) == 100


def test_delete_one_of_two_submissions(db_session: Session, insert_submissions: Callable) -> None:
    insert_submissions(2)

    delete_submission_by_id(db_session, "test_id-1")

    assert get_submission_by_id(db_session, "test_id-2")
    with pytest.raises(AttributeError):
        get_submission_by_id(db_session, "test_id-1")
