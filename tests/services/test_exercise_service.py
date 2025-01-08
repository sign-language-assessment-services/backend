from unittest.mock import Mock, patch

from app.services.exercise_service import ExerciseService
from tests.data.models.exercises import exercise_1, exercise_2


@patch(
    "app.services.exercise_service.get_exercise",
    return_value=exercise_1
)
def test_get_exercise_by_id(mocked_get_exercise, exercise_service: ExerciseService) -> None:
    exercise_id = mocked_get_exercise.return_value.id
    mocked_session = Mock()

    exercise = exercise_service.get_exercise_by_id(mocked_session, exercise_id)

    assert exercise.id == exercise_id
    assert exercise.points == mocked_get_exercise.return_value.points
    assert exercise.question == mocked_get_exercise.return_value.question
    assert exercise.question_type == mocked_get_exercise.return_value.question_type
    mocked_get_exercise.assert_called_once_with(session=mocked_session, _id=exercise_id)


@patch(
    "app.services.exercise_service.list_exercises",
    return_value=[exercise_1, exercise_2]
)
def test_list_exercises(mocked_list_exercise, exercise_service: ExerciseService) -> None:
    mocked_session = Mock()

    exercises = exercise_service.list_exercises(mocked_session)

    assert len(exercises) == len(mocked_list_exercise.return_value)
    for result, expected in zip(exercises, mocked_list_exercise.return_value):
        assert result.id == expected.id
        assert result.points == expected.points
        assert result.question == expected.question
        assert result.question_type == expected.question_type
    mocked_list_exercise.assert_called_once_with(session=mocked_session)
