from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from minio.datatypes import Object as MinioObject
from minio.error import MinioException

from app.core.models.bucket_object import BucketObject
from app.core.models.minio_location import MinioLocation
from app.services.object_storage_client import ObjectStorageClient


def test_http_exception_is_called_on_minio_errors(settings: Mock) -> None:
    object_storage_client = ObjectStorageClient(settings)
    object_storage_client.minio = Mock()
    object_storage_client.minio.get_presigned_url.side_effect = MinioException()

    with pytest.raises(HTTPException):
        location = MinioLocation(bucket=settings.bucket_name, key="123")
        object_storage_client.get_presigned_url(location=location)


def test_presigned_url_is_returned(settings: Mock) -> None:
    object_storage_client = ObjectStorageClient(settings)
    object_storage_client.minio = Mock()
    object_storage_client.minio.get_presigned_url.return_value = "presigned-url"

    location = MinioLocation(bucket=settings.bucket_name, key="123")
    result = object_storage_client.get_presigned_url(location=location)

    assert result == "presigned-url"


def test_list_folders_adds_an_trailing_slash(settings: Mock) -> None:
    object_storage_client = ObjectStorageClient(settings)
    object_storage_client.minio = Mock()

    with pytest.raises(TypeError):
        object_storage_client.list_folders(
            bucket_name=settings.data_bucket_name,
            folder="testfolder"
        )

    object_storage_client.minio.list_objects.assert_called_once_with(
        bucket_name=settings.data_bucket_name,
        prefix="testfolder/"
    )


def test_list_folders_returns_only_folders(settings: Mock, minio_data: list[MinioObject]) -> None:
    object_storage_client = ObjectStorageClient(settings)
    object_storage_client.minio = Mock()
    object_storage_client.minio.list_objects.return_value = minio_data

    result = object_storage_client.list_folders(settings.data_bucket_name, "any")

    assert result == ["folder01", "folder02"]


def test_list_files_adds_an_trailing_slash(settings: Mock) -> None:
    object_storage_client = ObjectStorageClient(settings)
    object_storage_client.minio = Mock()

    with pytest.raises(TypeError):
        object_storage_client.list_files(
            bucket_name=settings.data_bucket_name,
            folder="testfolder"
        )

    object_storage_client.minio.list_objects.assert_called_once_with(
        bucket_name=settings.data_bucket_name,
        prefix="testfolder/",
        include_user_meta=True
    )


def test_list_files_returns_only_files(settings: Mock, minio_data: list[MinioObject]) -> None:
    object_storage_client = ObjectStorageClient(settings)
    object_storage_client.minio = Mock()
    object_storage_client.minio.list_objects.return_value = minio_data

    result = object_storage_client.list_files(settings.data_bucket_name, "any")

    assert result == [
        BucketObject(name="file01", content_type="foo"),
        BucketObject(name="file02", content_type="foo")
    ]
