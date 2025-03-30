from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.core.models.assessment_submission import AssessmentSubmission
from app.database.exceptions import EntryNotFoundError
from app.database.tables.assessment_submissions import DbAssessmentSubmission
from app.repositories.assessment_submissions import (
    add_assessment_submission, delete_assessment_submission, get_assessment_submission,
    list_assessment_submissions, update_assessment_submission
)
from tests.database.data_inserts import (
    insert_assessment, insert_assessment_submission
)
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
