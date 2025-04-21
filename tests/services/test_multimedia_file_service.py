from unittest.mock import MagicMock, Mock, patch

from app.services import multimedia_file_service as multimedia_file_service_module
from app.services.multimedia_file_service import MultimediaFileService, get_multimedia_file
from tests.data.models.multimedia_files import multimedia_file_choice_1


@patch.object(
    multimedia_file_service_module, get_multimedia_file.__name__,
    return_value=multimedia_file_choice_1
)
def test_get_multimedia_file_by_id(
        mocked_get_multimedia_file: MagicMock,
        multimedia_file_service: MultimediaFileService
) -> None:
    multimedia_file_id = mocked_get_multimedia_file.return_value.id
    mocked_session = Mock()

    multimedia_file = multimedia_file_service.get_multimedia_file_by_id(mocked_session, multimedia_file_id)

    assert multimedia_file.id == multimedia_file_id
    assert multimedia_file.location == mocked_get_multimedia_file.return_value.location
    assert multimedia_file.media_type == mocked_get_multimedia_file.return_value.media_type
    mocked_get_multimedia_file.assert_called_once_with(session=mocked_session, _id=multimedia_file_id)
