from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.models.assessment_submission import AssessmentSubmission
from app.database.exceptions import EntryNotFoundError
from app.database.tables.assessment_submissions import DbAssessmentSubmission
from app.repositories.assessment_submissions import (
    add_assessment_submission, delete_assessment_submission, get_assessment_submission,
    list_assessment_submissions, update_assessment_submission
)
from tests.data.models.users import test_taker_1, test_taker_2
from tests.database.data_inserts import insert_assessment, insert_assessment_submission
from tests.database.utils import table_count


def test_add_assessment_submission(db_session: Session) -> None:
    user_id = uuid4()
    assessment = insert_assessment(session=db_session)
    assessment_submission = AssessmentSubmission(
        user_id=user_id,
        assessment_id=assessment.get("id")
    )

    add_assessment_submission(session=db_session, submission=assessment_submission)

    result = db_session.get(DbAssessmentSubmission, assessment_submission.id)
    assert result.id == assessment_submission.id
    assert result.created_at == assessment_submission.created_at
    assert result.user_id == assessment_submission.user_id
    assert result.score == assessment_submission.score
    assert result.finished_at == assessment_submission.finished_at
    assert result.assessment_id == assessment_submission.assessment_id
    assert table_count(db_session, DbAssessmentSubmission) == 1


def test_get_assessment_submission_by_id(db_session: Session) -> None:
    assessment_id = insert_assessment(session=db_session).get("id")
    assessment_submission = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment_id
    )

    result = get_assessment_submission(session=db_session, _id=assessment_submission.get("id"))

    assert result.id == assessment_submission.get("id")
    assert result.created_at == assessment_submission.get("created_at")
    assert result.user_id == assessment_submission.get("user_id")
    assert result.score == assessment_submission.get("score")
    assert result.finished_at == assessment_submission.get("finished_at")
    assert result.assessment_id == assessment_submission.get("assessment_id")
    assert table_count(db_session, DbAssessmentSubmission) == 1


def test_get_assessment_submission_by_id_returns_none_if_not_found(db_session: Session) -> None:
    result = get_assessment_submission(session=db_session, _id=uuid4())

    assert result is None


def test_list_no_assessment_submissions(db_session: Session) -> None:
    result = list_assessment_submissions(session=db_session)

    assert result == []


def test_list_multiple_assessment_submissions(db_session: Session) -> None:
    assessment_id = insert_assessment(session=db_session).get("id")
    for i in range(100):
        insert_assessment_submission(
            session=db_session,
            assessment_id=assessment_id
        )

    result = list_assessment_submissions(session=db_session)

    assert len(result) == 100
    assert table_count(db_session, DbAssessmentSubmission) == 100


def test_list_assessment_submissions_with_filter(db_session: Session) -> None:
    assessment_id = insert_assessment(session=db_session).get("id")
    for _ in range(10):
        insert_assessment_submission(
            session=db_session,
            assessment_id=assessment_id,
            user_id=test_taker_1.id
        )
    for _ in range(100):
        insert_assessment_submission(
            session=db_session,
            assessment_id=assessment_id
        )

    result = list_assessment_submissions(session=db_session, user_id=test_taker_1.id)

    assert len(result) == 10
    assert all(submission.user_id == test_taker_1.id for submission in result)
    assert table_count(db_session, DbAssessmentSubmission) == 110


@pytest.mark.parametrize("pick", ["best", "latest"])
def test_list_assessment_submissions_with_pick_has_only_one_result(db_session: Session, pick: str) -> None:
    assessment_id = insert_assessment(session=db_session).get("id")
    for _ in range(10):
        insert_assessment_submission(
            session=db_session,
            assessment_id=assessment_id
        )

    result = list_assessment_submissions(session=db_session, pick_strategy=pick)

    assert len(result) == 1
    assert table_count(db_session, DbAssessmentSubmission) == 10


def test_list_best_assessment_submissions(db_session: Session) -> None:
    assessment_id = insert_assessment(session=db_session).get("id")
    for num in range(10):
        insert_assessment_submission(
            session=db_session,
            assessment_id=assessment_id,
            score=float(num/2)
        )
    insert_assessment_submission(  # later insert with lower score
        session=db_session,
        assessment_id=assessment_id,
        score=4.4
    )

    result = list_assessment_submissions(session=db_session, pick_strategy="best")

    assert len(result) == 1
    assert result[0].score == 4.5


def test_list_latest_assessment_submissions(db_session: Session) -> None:
    assessment_id = insert_assessment(session=db_session).get("id")
    start_date = datetime(2000, 1, 1, 12, tzinfo=UTC)
    for num in range(10):
        insert_assessment_submission(
            session=db_session,
            assessment_id=assessment_id,
            created_at=start_date + timedelta(minutes=num),
        )

    result = list_assessment_submissions(session=db_session, pick_strategy="latest")

    assert len(result) == 1
    assert result[0].created_at == start_date + timedelta(minutes=9)


@pytest.mark.parametrize(
    "user_id, pick_strategy, expected_score, expected_date", [
        (None, "best", 1.0, datetime(2000, 1, 1, 3, tzinfo=UTC)),
        (None, "latest", 0, datetime(2000, 1, 1, 12, tzinfo=UTC)),
        (test_taker_1.id, "best", 8/9, datetime(2000, 1, 1, 4, tzinfo=UTC)),
        (test_taker_1.id, "latest", 0, datetime(2000, 1, 1, 12, tzinfo=UTC)),
        (test_taker_2.id, "best", 1.0, datetime(2000, 1, 1, 3, tzinfo=UTC)),
        (test_taker_2.id, "latest", 1/9, datetime(2000, 1, 1, 11, tzinfo=UTC))
    ]
)
def test_list_assessment_submissions_with_filter_and_pick(
        db_session: Session,
        user_id: UUID,
        pick_strategy: str,
        expected_score: float,
        expected_date: datetime
) -> None:
    assessment = insert_assessment(session=db_session)
    for n in range(10):
        insert_assessment_submission(
            session=db_session,
            assessment_id=assessment.get("id"),
            user_id=test_taker_1.id if n % 2 == 0 else test_taker_2.id,
            created_at=datetime(2000, 1, 1, 12, tzinfo=UTC) - timedelta(hours=n),
            score=n/9
        )

    result = list_assessment_submissions(
        session=db_session,
        user_id=user_id,
        pick_strategy=pick_strategy
    )

    assert len(result) == 1
    assert result[0].score == expected_score
    assert result[0].created_at == expected_date
    assert table_count(db_session, DbAssessmentSubmission) == 10


def test_update_assessment_submission(db_session: Session) -> None:
    assessment = insert_assessment(session=db_session)
    assessment_submission = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment.get("id")
    )

    update_assessment_submission(
        session=db_session,
        _id=assessment_submission.get("id"),
        **{"score": 1}
    )

    result = db_session.get(DbAssessmentSubmission, assessment_submission.get("id"))
    assert result.id == assessment_submission.get("id")
    assert result.created_at == assessment_submission.get("created_at")
    assert result.user_id == assessment_submission.get("user_id")
    assert result.score != assessment_submission.get("score")
    assert result.score == 1
    assert result.finished_at == assessment_submission.get("finished_at")
    assert result.assessment_id == assessment_submission.get("assessment_id")
    assert table_count(db_session, DbAssessmentSubmission) == 1


def test_delete_assessment_submission(db_session: Session) -> None:
    assessment = insert_assessment(session=db_session)
    assessment_submission = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment.get("id")
    )

    delete_assessment_submission(session=db_session, _id=assessment_submission.get("id"))

    result = db_session.get(DbAssessmentSubmission, assessment_submission.get("id"))
    assert result is None
    assert table_count(db_session, DbAssessmentSubmission) == 0


def test_delete_one_of_two_assessment_submissions(db_session: Session) -> None:
    assessment = insert_assessment(session=db_session)
    assessment_submission = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment.get("id")
    )
    insert_assessment_submission(
        session=db_session,
        assessment_id=assessment.get("id")
    )

    delete_assessment_submission(session=db_session, _id=assessment_submission.get("id"))

    result = db_session.get(DbAssessmentSubmission, assessment_submission.get("id"))
    assert result is None
    assert table_count(db_session, DbAssessmentSubmission) == 1


def test_delete_not_existing_assessment_submission_should_fail(db_session: Session) -> None:
    with pytest.raises(EntryNotFoundError, match=r"has no entry with id"):
        delete_assessment_submission(session=db_session, _id=uuid4())


def test_add_finished_assessment_submission_is_possible(db_session: Session) -> None:
    user_id = uuid4()
    assessment = insert_assessment(session=db_session)
    assessment_submission = AssessmentSubmission(
        user_id=user_id,
        assessment_id=assessment.get("id"),
        finished=True,
        finished_at=datetime(2000, 1, 1, 13, tzinfo=UTC)
    )

    db_assessment_submission = insert_assessment_submission(
        session=db_session,
        assessment_id=assessment.get("id"),
        finished=assessment_submission.finished,
        finished_at=assessment_submission.finished_at
    )

    result = db_session.get(DbAssessmentSubmission, db_assessment_submission.get("id"))
    assert result.id == db_assessment_submission.get("id")
    assert result.finished is True
    assert result.finished_at == assessment_submission.finished_at


def test_add_finished_assessment_submission_fails_if_finished_at_not_given(db_session: Session) -> None:
    user_id = uuid4()
    assessment = insert_assessment(session=db_session)
    assessment_submission = AssessmentSubmission(
        user_id=user_id,
        assessment_id=assessment.get("id"),
        finished=True
    )

    with pytest.raises(
            IntegrityError,
            match=r'violates check constraint "check_finished_at_only_when_finished"'
    ):
        insert_assessment_submission(
            session=db_session,
            assessment_id=assessment.get("id"),
            finished=assessment_submission.finished,
        )
