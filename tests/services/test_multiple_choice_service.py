from unittest.mock import MagicMock, Mock, patch

from data.models.choices import choice_1, choice_2, choice_3, choice_4

from app.services import multiple_choice_service as multiple_choice_service_module
from app.services.multiple_choice_service import MultipleChoiceService, add_multiple_choice


@patch.object(
    multiple_choice_service_module, add_multiple_choice.__name__,
)
def test_create_multiple_choice(
        mocked_add_multiple_choice: MagicMock,
        multiple_choice_service: MultipleChoiceService
) -> None:
    mocked_session = Mock()
    mocked_get_choice_by_id = Mock(side_effect=[choice_1, choice_2, choice_3, choice_4])
    multiple_choice_service.choice_service.get_choice_by_id = mocked_get_choice_by_id
    choices = [choice_1, choice_2, choice_3, choice_4]

    multiple_choice = multiple_choice_service.create_multiple_choice(
        session=mocked_session,
        choice_ids=[choice.id for choice in choices],
        correct_choice_ids=[choice_1.id]
    )

    mocked_add_multiple_choice.assert_called_once_with(
        session=mocked_session,
        multiple_choice=multiple_choice
    )
    assert multiple_choice.choices[0].id == choices[0].id
    assert multiple_choice.choices[0].is_correct == True
    assert multiple_choice.choices[1].id == choices[1].id
    assert multiple_choice.choices[1].is_correct == False
    assert multiple_choice.choices[2].id == choices[2].id
    assert multiple_choice.choices[2].is_correct == False
    assert multiple_choice.choices[3].id == choices[3].id
    assert multiple_choice.choices[3].is_correct == False


def test_get_multiple_choice_by_id() -> None:
    pass  # TODO


def test_list_multiple_choices() -> None:
    pass  # TODO
