from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.core.models.choice import Choice
from app.core.models.exercise import Exercise
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.primer import Primer
from app.core.models.question import Question
from app.core.models.question_type import QuestionType
from app.database.tables.assessments import DbAssessment
from app.database.tables.exercises import DbExercise
from app.database.tables.primers import DbPrimer
from app.database.tables.tasks import DbTask
from app.repositories.assessments import (
    add_assessment, delete_assessment, get_assessment, list_assessments, update_assessment
)
from tests.database.data_inserts import (
    connect_assessment_with_tasks, insert_assessment, insert_bucket_object,
    insert_choice, insert_exercise, insert_multiple_choice, insert_primer
)
from tests.database.utils import table_count


def test_add_assessment(db_session: Session) -> None:
    assessment = Assessment(name="Test Assessment")

    add_assessment(session=db_session, assessment=assessment)
    
    result = db_session.get(DbAssessment, assessment.id)
    assert result.id == assessment.id
    assert result.created_at == assessment.created_at
    assert result.name == assessment.name
    assert result.deadline == assessment.deadline
    assert result.max_attempts == assessment.max_attempts
    assert table_count(db_session, DbAssessment) == 1


@pytest.mark.skip(
    reason="Adding assessment with tasks is not working as intended. "
           "The test should work with the asserts at the end of the test. "
           "Also think about ommitting the inserts at the beginning."
)
def test_add_assessment_with_tasks(db_session: Session) -> None:
    bucket_object = insert_bucket_object(session=db_session, filename="testfile.mpg")
    choice_object = insert_choice(session=db_session, bucket_object_id=bucket_object.get("id"))
    multiple_choice_object = insert_multiple_choice(session=db_session)
    multimedia_file = MultimediaFile(
        id=bucket_object.get("id"),
        location=MinioLocation(
            bucket=bucket_object.get("bucket"),
            key=bucket_object.get("key")
        ),
        media_type=MediaType.VIDEO
    )
    assessment = Assessment(
        name="Test Assessment",
        tasks=[
            Primer(
                content=multimedia_file
            ),
            Exercise(
                points=1,
                question=Question(content=multimedia_file),
                question_type=QuestionType(
                    content=MultipleChoice(
                        id=multiple_choice_object.get("id"),
                        choices=[
                            Choice(
                                id=choice_object.get("id"),
                                content=multimedia_file,
                            )
                        ]
                    )
                )
            )
        ]
    )

    add_assessment(session=db_session, assessment=assessment)

    result = db_session.get(DbAssessment, assessment.id)
    assert result.id == assessment.id
    assert result.created_at == assessment.created_at
    assert result.name == assessment.name
    assert result.deadline == assessment.deadline
    assert result.max_attempts == assessment.max_attempts
    assert table_count(db_session, DbAssessment) == 1
    # TODO: make following asserts work
    assert result.tasks[0].id == assessment.tasks[0].id
    assert result.tasks[0].created_at == assessment.tasks[0].created_at
    assert result.tasks[0].task_type == "primer"
    assert table_count(db_session, DbTask) == 2
    assert table_count(db_session, DbPrimer) == 1
    assert table_count(db_session, DbExercise) == 1


def test_get_assessment_by_id(db_session: Session) -> None:
    assessment = insert_assessment(session=db_session, name="Test Assessment")

    result = get_assessment(session=db_session, _id=assessment.get("id"))

    assert result.id == assessment.get("id")
    assert result.created_at == assessment.get("created_at")
    assert result.name == assessment.get("name")
    assert result.deadline == assessment.get("deadline")
    assert result.max_attempts == assessment.get("max_attempts")
    assert table_count(db_session, DbAssessment) == 1


def test_get_assessment_with_tasks(db_session: Session) -> None:
    multimedia_file = insert_bucket_object(session=db_session, filename="testfile.mpg")
    primer = insert_primer(session=db_session, bucket_object_id=multimedia_file.get("id"))
    multiple_choice = insert_multiple_choice(session=db_session)
    exercise = insert_exercise(
        session=db_session,
        bucket_object_id=multimedia_file.get("id"),
        multiple_choice_id=multiple_choice.get("id")
    )
    assessment = insert_assessment(session=db_session, name="Test Assessment")
    connect_assessment_with_tasks(
        session=db_session,
        assessment_id=assessment.get("id"),
        task_ids=[primer.get("id"), exercise.get("id")]
    )

    result = get_assessment(session=db_session, _id=assessment.get("id"))

    assert result.id == assessment.get("id")
    assert result.created_at == assessment.get("created_at")
    assert result.name == assessment.get("name")
    assert result.deadline == assessment.get("deadline")
    assert result.max_attempts == assessment.get("max_attempts")
    assert table_count(db_session, DbAssessment) == 1
    assert table_count(db_session, DbTask) == 2
    assert len(result.tasks) == 2
    assert result.tasks[0].id == primer.get("id")
    assert result.tasks[0].created_at == primer.get("created_at")
    assert isinstance(result.tasks[0], Primer)
    assert result.tasks[1].id == exercise.get("id")
    assert result.tasks[1].created_at == exercise.get("created_at")
    assert isinstance(result.tasks[1], Exercise)


def test_get_assessment_by_id_returns_none_if_not_found(db_session: Session) -> None:
    result = get_assessment(session=db_session, _id=uuid4())

    assert result is None


def test_list_no_assessments(db_session: Session) -> None:
    result = list_assessments(session=db_session)

    assert result == []
    assert table_count(db_session, DbAssessment) == 0


def test_list_multiple_assessments(db_session: Session) -> None:
    for i in range(100):
        insert_assessment(session=db_session, name=f"Test Assessment {i}")

    result = list_assessments(db_session)

    assert len(result) == 100
    assert table_count(db_session, DbAssessment) == 100


def test_update_assessment(db_session: Session) -> None:
    assessment = insert_assessment(session=db_session)

    updated_name = "Updated Assessment"
    update_assessment(
        session=db_session,
        _id=assessment.get("id"),
        **{"name": updated_name}
    )

    result = db_session.get(DbAssessment, assessment.get("id"))
    assert result.id == assessment.get("id")
    assert result.created_at == assessment.get("created_at")
    assert result.name == updated_name
    assert result.deadline == assessment.get("deadline")
    assert result.max_attempts == assessment.get("max_attempts")
    assert table_count(db_session, DbAssessment) == 1


def test_delete_assessment(db_session: Session) -> None:
    assessment_id = insert_assessment(session=db_session).get("id")

    delete_assessment(session=db_session, _id=assessment_id)

    result = db_session.get(DbAssessment, assessment_id)
    assert result is None
    assert table_count(db_session, DbAssessment) == 0


def test_delete_one_of_two_assessments(db_session: Session) -> None:
    assessment_id = insert_assessment(session=db_session, name="Test 1").get("id")
    insert_assessment(session=db_session, name="Test 2")

    delete_assessment(session=db_session, _id=assessment_id)

    result = db_session.get(DbAssessment, assessment_id)
    assert result is None
    assert table_count(db_session, DbAssessment) == 1
