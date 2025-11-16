from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest

from app.services import multiple_choice_service as multiple_choice_service_module
from app.services.exceptions.not_found import MultipleChoiceNotFoundException
from app.services.multiple_choice_service import (
    MultipleChoiceService, add_multiple_choice, get_multiple_choice, list_multiple_choices
)
from tests.data.models.choices import (
    associated_choice_1, associated_choice_2, associated_choice_3, associated_choice_4, choice_1,
    choice_2, choice_3, choice_4
)
from tests.data.models.multiple_choices import multiple_choice_1, multiple_choice_2


@patch.object(multiple_choice_service_module, add_multiple_choice.__name__)
def test_create_multiple_choice(
        mocked_add_multiple_choice: MagicMock,
        multiple_choice_service: MultipleChoiceService
) -> None:
    mocked_session = Mock()
    mocked_get_choice_by_id = Mock(side_effect=[choice_1, choice_2, choice_3, choice_4])
    multiple_choice_service.choice_service.get_choice_by_id = mocked_get_choice_by_id
    choices = [associated_choice_1, associated_choice_2, associated_choice_3, associated_choice_4]

    multiple_choice = multiple_choice_service.create_multiple_choice(
        session=mocked_session,
        choice_ids=[choice.id for choice in choices],
        correct_choice_ids=[associated_choice_1.id]
    )

    mocked_add_multiple_choice.assert_called_once_with(
        session=mocked_session,
        multiple_choice=multiple_choice
    )
    assert multiple_choice.choices[0].id == choices[0].id
    assert multiple_choice.choices[0].is_correct == True
    assert multiple_choice.choices[0].position == 1
    assert multiple_choice.choices[1].id == choices[1].id
    assert multiple_choice.choices[1].is_correct == False
    assert multiple_choice.choices[1].position == 2
    assert multiple_choice.choices[2].id == choices[2].id
    assert multiple_choice.choices[2].is_correct == False
    assert multiple_choice.choices[2].position == 3
    assert multiple_choice.choices[3].id == choices[3].id
    assert multiple_choice.choices[3].is_correct == False
    assert multiple_choice.choices[3].position == 4


@patch.object(
    multiple_choice_service_module, get_multiple_choice.__name__,
    return_value=multiple_choice_1
)
def test_get_multiple_choice_by_id(
        mocked_get_multiple_choice: MagicMock,
        multiple_choice_service: MultipleChoiceService
) -> None:
    multiple_choice_id = mocked_get_multiple_choice.return_value.id
    mocked_session = Mock()

    multiple_choice = multiple_choice_service.get_multiple_choice_by_id(
        session=mocked_session,
        multiple_choice_id=multiple_choice_id
    )

    mocked_get_multiple_choice.assert_called_once_with(session=mocked_session, _id=multiple_choice_id)
    assert multiple_choice.id == multiple_choice_id
    assert multiple_choice.choices == mocked_get_multiple_choice.return_value.choices


@patch.object(
    multiple_choice_service_module, get_multiple_choice.__name__,
    return_value=None
)
def test_get_non_existing_multiple_choice_by_id(
        mocked_get_multiple_choice: MagicMock,
        multiple_choice_service: MultipleChoiceService
) -> None:
    mocked_session = Mock()
    non_existing_id = uuid4()

    with pytest.raises(MultipleChoiceNotFoundException):
        multiple_choice_service.get_multiple_choice_by_id(mocked_session, non_existing_id)

    mocked_get_multiple_choice.assert_called_once_with(session=mocked_session, _id=non_existing_id)


@patch.object(
    multiple_choice_service_module, list_multiple_choices.__name__,
    return_value=[multiple_choice_1, multiple_choice_2]
)
def test_list_multiple_choice_by_id(
        mocked_list_multiple_choice: MagicMock,
        multiple_choice_service: MultipleChoiceService
) -> None:
    mocked_session = Mock()

    multiple_choices = multiple_choice_service.list_multiple_choices(
        session=mocked_session
    )

    mocked_list_multiple_choice.assert_called_once_with(session=mocked_session)
    assert multiple_choices == mocked_list_multiple_choice.return_value
