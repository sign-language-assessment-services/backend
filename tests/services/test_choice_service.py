from unittest.mock import MagicMock, Mock, patch

from app.services import choice_service as choice_service_module
from app.services.choice_service import ChoiceService, add_choice, get_choice, list_choices
from tests.data.models.choices import choice_1, choice_2
from tests.data.models.multimedia_files import multimedia_file_choice_1


@patch.object(
    choice_service_module, add_choice.__name__,
)
def test_create_choice(
        mocked_add_choice: MagicMock,
        choice_service: ChoiceService
) -> None:
    mocked_session = Mock()
    mocked_get_multimedia_file_by_id = Mock(return_value=multimedia_file_choice_1)
    choice_service.multimedia_file_service.get_multimedia_file_by_id = mocked_get_multimedia_file_by_id

    choice = choice_service.create_choice(
        session=mocked_session,
        multimedia_file_id=multimedia_file_choice_1.id,
    )

    mocked_add_choice.assert_called_once_with(
        session=mocked_session,
        choice=choice
    )
    assert choice.content == multimedia_file_choice_1


@patch.object(
    choice_service_module, get_choice.__name__,
    return_value=choice_1
)
def test_get_choice_by_id(
        mocked_get_choice: MagicMock,
        choice_service: ChoiceService
) -> None:
    choice_id = mocked_get_choice.return_value.id
    mocked_session = Mock()

    choice = choice_service.get_choice_by_id(
        session=mocked_session,
        choice_id=choice_id
    )

    mocked_get_choice.assert_called_once_with(session=mocked_session, _id=choice_id)
    assert choice.id == choice_id


@patch.object(
    choice_service_module, list_choices.__name__,
    return_value=[choice_1, choice_2]
)
def test_list_choice_by_id(
        mocked_list_choice: MagicMock,
        choice_service: ChoiceService
) -> None:
    mocked_session = Mock()

    choices = choice_service.list_choices(
        session=mocked_session
    )

    mocked_list_choice.assert_called_once_with(session=mocked_session)
    assert choices == mocked_list_choice.return_value
