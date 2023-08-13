from unittest.mock import Mock

import pytest
from minio.datatypes import Object as MinioObject

from app.core.models.bucket_object import BucketObject


@pytest.fixture
def object_storage_folders() -> list[str]:
    return ["00", "01"]


@pytest.fixture
def object_storage_files() -> list[list[BucketObject]]:
    return [
        [
            BucketObject(
                name="frage",
                content_type="video/mp4"
            ),
            BucketObject(
                name="video_antwort_richtig",
                content_type="video/mp4"
            ),
            BucketObject(
                name="bild_antwort",
                content_type="image/jpeg"
            )
        ],
        [
            BucketObject(
                name="video",
                content_type="video/mp4"
            )
        ]
    ]


@pytest.fixture
def object_storage_client(object_storage_files: list[list[BucketObject]], object_storage_folders: list[str]) -> Mock:
    object_storage_client = Mock()
    object_storage_client.get_presigned_url.return_value = "http://some-url"
    object_storage_client.list_files.side_effect = object_storage_files
    object_storage_client.list_folders.return_value = object_storage_folders
    return object_storage_client


@pytest.fixture
def minio_data() -> list[MinioObject]:
    return [
        MinioObject(bucket_name="testbucket", object_name="folder01/"),
        MinioObject(bucket_name="testbucket", object_name="folder02/"),
        MinioObject(
            bucket_name="testbucket",
            object_name="file01",
            metadata={"content-type": "foo"}
        ),
        MinioObject(
            bucket_name="testbucket",
            object_name="file02",
            metadata={"content-type": "foo"}
        )
    ]
