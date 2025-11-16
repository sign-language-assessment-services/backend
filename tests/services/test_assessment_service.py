from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest

from app.services import assessment_service as assessment_service_module
from app.services.assessment_service import (
    AssessmentService, add_assessment, get_assessment, list_assessments
)
from app.services.exceptions.not_found import AssessmentNotFoundException
from app.services.task_service import TaskService
from tests.data.models.assessments import assessment_1, assessment_2
from tests.data.models.exercises import exercise_1
from tests.data.models.primers import primer_1


@patch.object(assessment_service_module, add_assessment.__name__)
def test_create_assessment_without_tasks(
        mocked_add_assessment: MagicMock,
        assessment_service: AssessmentService
) -> None:
    mocked_session = Mock()

    assessment = assessment_service.create_assessment(
        session=mocked_session,
        name=assessment_1.name
    )

    assert assessment.name == assessment_1.name
    mocked_add_assessment.assert_called_once_with(
        session=mocked_session,
        assessment=assessment
    )


@patch.object(assessment_service_module, add_assessment.__name__)
@patch.object(TaskService, TaskService.get_task_by_id.__name__, side_effect=[primer_1, exercise_1])
def test_create_assessment_with_tasks(
        _: MagicMock,
        mocked_add_assessment: MagicMock,
        assessment_service: AssessmentService
) -> None:
    mocked_session = Mock()

    assessment = assessment_service.create_assessment(
        session=mocked_session,
        name=assessment_1.name,
        task_ids=[assessment_1.tasks[0].id, assessment_1.tasks[1].id]
    )

    assert assessment.name == assessment_1.name
    mocked_add_assessment.assert_called_once_with(
        session=mocked_session,
        assessment=assessment
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
