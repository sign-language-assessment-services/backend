from unittest.mock import MagicMock, Mock, patch

from app.services import task_service as task_service_module
from app.services.task_service import TaskService, get_task
from tests.data.models.exercises import exercise_1
from tests.data.models.primers import primer_1


@patch.object(task_service_module, get_task.__name__, return_value=primer_1)
def test_get_primer_task(
        mocked_get_task: MagicMock,
        task_service: TaskService
) -> None:
    mocked_session = Mock()
    primer = task_service.get_task_by_id(
        session=mocked_session,
        task_id=primer_1.id
    )

    mocked_get_task.assert_called_once_with(
        session=mocked_session,
        _id=primer_1.id
    )
    assert primer.id == primer_1.id


@patch.object(task_service_module, get_task.__name__, return_value=exercise_1)
def test_get_exercise_task(
        mocked_get_task: MagicMock,
        task_service: TaskService
) -> None:
    mocked_session = Mock()
    exercise = task_service.get_task_by_id(
        session=mocked_session,
        task_id=exercise_1.id
    )

    mocked_get_task.assert_called_once_with(
        session=mocked_session,
        _id=exercise_1.id
    )
    assert exercise.id == exercise_1.id
