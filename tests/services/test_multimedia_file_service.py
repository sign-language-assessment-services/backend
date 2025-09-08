from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.services import multimedia_file_service as multimedia_file_service_module
from app.services.multimedia_file_service import (
    MultimediaFileService, add_multimedia_file, get_multimedia_file, list_multimedia_files
)
from tests.data.models.multimedia_files import multimedia_file_choice_1, multimedia_file_choice_2


@patch.object(multimedia_file_service_module, add_multimedia_file.__name__)
def test_create_multimedia_file(
        mocked_add_multimedia_file: MagicMock,
        multimedia_file_service: MultimediaFileService,
        tmp_path: Path
) -> None:
    mocked_session = Mock()
    mocked_add_object_storage = Mock()
    multimedia_file_service.object_storage_client.add_object = mocked_add_object_storage
    test_file_path = tmp_path / "test.mp4"
    test_file_path.write_text("video_input")
    test_file = open(test_file_path, mode="rb")

    multimedia_file = multimedia_file_service.create_multimedia_file(
        session=mocked_session,
        file=test_file,
        media_type=MediaType.VIDEO
    )

    mocked_add_object_storage.assert_called_once_with(
        location=MinioLocation(
            bucket=multimedia_file.location.bucket,
            key=multimedia_file.location.key
        ),
        data=test_file,
        media_type=MediaType.VIDEO
    )
    mocked_add_multimedia_file.assert_called_once_with(
        session=mocked_session,
        multimedia_file=multimedia_file
    )
    assert mocked_add_object_storage.call_args.kwargs["location"].bucket == multimedia_file_service.settings.data_bucket_name
    assert mocked_add_object_storage.call_args.kwargs["location"].key == str(multimedia_file.id)
    assert multimedia_file.media_type == MediaType.VIDEO


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


@patch.object(
    multimedia_file_service_module, list_multimedia_files.__name__,
    return_value=[multimedia_file_choice_1, multimedia_file_choice_2]
)
def test_list_multimedia_files(
        mocked_list_multimedia_file: MagicMock,
        multimedia_file_service: MultimediaFileService
) -> None:
    mocked_session = Mock()

    multimedia_files = multimedia_file_service.list_multimedia_files(mocked_session)

    mocked_list_multimedia_file.assert_called_once_with(session=mocked_session)
    assert multimedia_files == mocked_list_multimedia_file.return_value
