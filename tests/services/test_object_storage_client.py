import pytest
from fastapi import HTTPException
from minio.datatypes import Object as MinioObject
from minio.error import MinioException

from app.core.models.bucket_object import BucketObject
from app.core.models.minio_location import MinioLocation
from app.services.object_storage_client import ObjectStorageClient


def test_http_exception_is_called_on_minio_errors(storage_client_minio: ObjectStorageClient) -> None:
    storage_client_minio.minio.get_presigned_url.side_effect = MinioException()

    with pytest.raises(HTTPException):
        location = MinioLocation(bucket="testbucket", key="123")
        storage_client_minio.get_presigned_url(location=location)


def test_presigned_url_is_returned(storage_client_minio: ObjectStorageClient) -> None:
    storage_client_minio.minio.get_presigned_url.return_value = "presigned-url"

    location = MinioLocation(bucket="testbucket", key="123")
    result = storage_client_minio.get_presigned_url(location=location)

    assert result == "presigned-url"


def test_list_folders_adds_an_trailing_slash(storage_client_minio: ObjectStorageClient) -> None:
    with pytest.raises(TypeError):
        storage_client_minio.list_folders(
            bucket_name="testbucket",
            folder="testfolder"
        )

    storage_client_minio.minio.list_objects.assert_called_once_with(
        bucket_name="testbucket",
        prefix="testfolder/"
    )


def test_list_folders_returns_only_folders(
        storage_client_minio: ObjectStorageClient,
        minio_data: list[MinioObject]
) -> None:
    storage_client_minio.minio.list_objects.return_value = minio_data

    result = storage_client_minio.list_folders("testbucket", "foo")

    assert result == ["folder01", "folder02"]


def test_list_files_adds_an_trailing_slash(storage_client_minio: ObjectStorageClient) -> None:
    with pytest.raises(TypeError):
        storage_client_minio.list_files(
            bucket_name="testbucket",
            folder="testfolder"
        )

    storage_client_minio.minio.list_objects.assert_called_once_with(
        bucket_name="testbucket",
        prefix="testfolder/",
        include_user_meta=True
    )


def test_list_files_returns_only_files(
        storage_client_minio: ObjectStorageClient,
        minio_data: list[MinioObject]
) -> None:
    storage_client_minio.minio.list_objects.return_value = minio_data

    result = storage_client_minio.list_files("testbucket", "any")

    assert result == [
        BucketObject(name="file01", content_type="foo"),
        BucketObject(name="file02", content_type="foo")
    ]
