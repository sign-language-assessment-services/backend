from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.database.tables.assessments import DbAssessment
from app.database.tables.tasks import DbTask
from app.services import assessment_service as assessment_service_module
from app.services.assessment_service import (
    AssessmentService, add_entry, assessment_to_domain, get_assessment, list_assessments
)
from app.services.exceptions.not_found import AssessmentNotFoundException, TaskNotFoundException
from app.services.task_service import TaskService
from tests.data.models.assessments import assessment_1, assessment_2
from tests.data.models.exercises import exercise_1
from tests.data.models.primers import primer_1
from tests.database.data_inserts import (
    insert_bucket_object, insert_exercise, insert_multiple_choice, insert_primer
)


@patch.object(assessment_service_module, assessment_to_domain.__name__, return_value=assessment_1)
@patch.object(assessment_service_module, add_entry.__name__)
def test_create_assessment_without_tasks(
        mocked_add_entry: MagicMock,
        mocked_assessment_to_domain: MagicMock,
        assessment_service: AssessmentService
) -> None:
    mocked_session = Mock()

    assessment = assessment_service.create_assessment(
        session=mocked_session,
        name=assessment_1.name
    )

    assert assessment.name == assessment_1.name
    mocked_add_entry.assert_called_once()
    mocked_assessment_to_domain.assert_called_once()


@patch.object(assessment_service_module, assessment_to_domain.__name__, return_value=assessment_1)
@patch.object(assessment_service_module, add_entry.__name__)
@patch.object(TaskService, TaskService.get_task_by_id.__name__, side_effect=[primer_1, exercise_1])
def test_create_assessment_with_tasks(
        _: MagicMock,
        mocked_add_entry: MagicMock,
        mocked_assessment_to_domain: MagicMock,
        assessment_service: AssessmentService
) -> None:
    mocked_session = Mock()
    mocked_task = DbTask(id=uuid4(), task_type="primer")
    mocked_session.get.return_value = mocked_task
    
    db_assessment = DbAssessment(name=assessment_1.name)
    with patch.object(assessment_service_module, DbAssessment.__name__, return_value=db_assessment):
        assessment = assessment_service.create_assessment(
            session=mocked_session,
            name=assessment_1.name,
            task_ids=[assessment_1.tasks[0].id, assessment_1.tasks[1].id]
        )

    assert assessment.name == assessment_1.name
    assert len(db_assessment.tasks_link) == 2
    mocked_add_entry.assert_called_once()
    mocked_assessment_to_domain.assert_called_once()


def test_create_assessment_with_existing_tasks(
        db_session: Session,
        assessment_service: AssessmentService
) -> None:
    multimedia_file = insert_bucket_object(session=db_session, filename="testfile.mpg")
    primer = insert_primer(session=db_session, bucket_object_id=multimedia_file.get("id"))
    multiple_choice = insert_multiple_choice(session=db_session)
    exercise = insert_exercise(
        session=db_session,
        bucket_object_id=multimedia_file.get("id"),
        multiple_choice_id=multiple_choice.get("id")
    )

    assessment = assessment_service.create_assessment(
        session=db_session,
        name=assessment_1.name,
        task_ids=[primer.get("id"), exercise.get("id")]
    )

    assert assessment.name == assessment_1.name
    assert assessment.tasks[0].id == primer.get("id")
    assert assessment.tasks[1].id == exercise.get("id")
    assert len(assessment.tasks) == 2


def test_create_assessment_with_non_existing_tasks_fails(
        db_session: Session,
        assessment_service: AssessmentService
) -> None:
    with pytest.raises(TaskNotFoundException):
        assessment_service.create_assessment(
            session=db_session,
            name=assessment_1.name,
            task_ids=[uuid4(), uuid4()]
        )


@patch.object(
    assessment_service_module, get_assessment.__name__,
    return_value=assessment_1
)
def test_get_assessment_by_id(
        mocked_get_assessment: MagicMock,
        assessment_service: AssessmentService
) -> None:
    assessment_id = mocked_get_assessment.return_value.id
    mocked_session = Mock()

    assessment = assessment_service.get_assessment_by_id(mocked_session, assessment_id)

    assert assessment.id == assessment_id
    assert assessment.name == mocked_get_assessment.return_value.name
    mocked_get_assessment.assert_called_once_with(session=mocked_session, _id=assessment_id)


@patch.object(
    assessment_service_module, get_assessment.__name__,
    return_value=None
)
def test_get_non_existing_assessment_by_id(
        mocked_get_assessment: MagicMock,
        assessment_service: AssessmentService
) -> None:
    mocked_session = Mock()
    non_existing_id = uuid4()

    with pytest.raises(AssessmentNotFoundException):
        assessment_service.get_assessment_by_id(mocked_session, non_existing_id)

    mocked_get_assessment.assert_called_once_with(session=mocked_session, _id=non_existing_id)


@patch.object(
    assessment_service_module, list_assessments.__name__,
    return_value=[assessment_1, assessment_2]
)
def test_list_assessments(
        mocked_list_assessment: MagicMock,
        assessment_service: AssessmentService
) -> None:
    mocked_session = Mock()

    assessments = assessment_service.list_assessments(mocked_session)

    assert len(assessments) == len(mocked_list_assessment.return_value)
    for result, expected in zip(assessments, mocked_list_assessment.return_value):
        assert result.id == expected.id
        assert result.name == expected.name
    mocked_list_assessment.assert_called_once_with(session=mocked_session)
