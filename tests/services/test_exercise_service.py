from unittest.mock import MagicMock, Mock, patch

from app.services import exercise_service as exercise_service_module
from app.services.exercise_service import (
    ExerciseService, add_exercise, get_exercise, get_multimedia_file, get_multiple_choice,
    list_exercises
)
from tests.data.models.exercises import exercise_1, exercise_2
from tests.data.models.multimedia_files import multimedia_file_choice_1
from tests.data.models.multiple_choices import multiple_choice_1


@patch.object(exercise_service_module, get_multiple_choice.__name__, return_value=multiple_choice_1)
@patch.object(exercise_service_module, get_multimedia_file.__name__, return_value=multimedia_file_choice_1)
@patch.object(exercise_service_module, add_exercise.__name__)
def test_create_empty_exercise(
        mocked_add_exercise: MagicMock,
        mocked_get_multimedia_file: MagicMock,
        mocked_get_multiple_choice: MagicMock,
        exercise_service: ExerciseService
) -> None:
    mocked_session = Mock()

    exercise = exercise_service.create_exercise(
        session=mocked_session,
        points=1,
        multimedia_file_id=mocked_get_multimedia_file.id,
        multiple_choice_id=mocked_get_multiple_choice.id
    )

    mocked_add_exercise.assert_called_once_with(session=mocked_session, exercise=exercise)
    assert exercise.points == 1
    assert exercise.question.content == mocked_get_multimedia_file.return_value
    assert exercise.question_type.content == mocked_get_multiple_choice.return_value


@patch.object(
    exercise_service_module, get_exercise.__name__,
    return_value=exercise_1
)
def test_get_exercise_by_id(
        mocked_get_exercise: MagicMock,
        exercise_service: ExerciseService
) -> None:
    exercise_id = mocked_get_exercise.return_value.id
    mocked_session = Mock()

    exercise = exercise_service.get_exercise_by_id(mocked_session, exercise_id)

    assert exercise.id == exercise_id
    assert exercise.points == mocked_get_exercise.return_value.points
    assert exercise.question == mocked_get_exercise.return_value.question
    assert exercise.question_type == mocked_get_exercise.return_value.question_type
    mocked_get_exercise.assert_called_once_with(session=mocked_session, _id=exercise_id)


@patch.object(
    exercise_service_module, list_exercises.__name__,
    return_value=[exercise_1, exercise_2]
)
def test_list_exercises(
        mocked_list_exercise: MagicMock,
        exercise_service: ExerciseService
) -> None:
    mocked_session = Mock()

    exercises = exercise_service.list_exercises(mocked_session)

    assert len(exercises) == len(mocked_list_exercise.return_value)
    for result, expected in zip(exercises, mocked_list_exercise.return_value):
        assert result.id == expected.id
        assert result.points == expected.points
        assert result.question == expected.question
        assert result.question_type == expected.question_type
    mocked_list_exercise.assert_called_once_with(session=mocked_session)
