from unittest.mock import Mock

import pytest
from minio.datatypes import Object as MinioObject

from app.core.models.bucket_object import BucketObject
from app.services.assessment_service import AssessmentService
from app.services.object_storage_client import ObjectStorageClient

StorageFiles = list[list[BucketObject]]


@pytest.fixture
def storage_folders() -> list[str]:
    return ["00", "01"]


@pytest.fixture
def storage_files() -> StorageFiles:
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
def storage_client(storage_files: StorageFiles, storage_folders: list[str]) -> Mock:
    object_storage_client = Mock()
    object_storage_client.get_presigned_url.return_value = "http://some-url"
    object_storage_client.list_files.side_effect = storage_files
    object_storage_client.list_folders.return_value = storage_folders
    return object_storage_client


@pytest.fixture
def storage_client_minio(settings: Mock) -> ObjectStorageClient:
    object_storage_client = ObjectStorageClient(settings)
    object_storage_client.minio = Mock()
    return object_storage_client


@pytest.fixture
def assessment_service(storage_client: Mock, settings: Mock) -> AssessmentService:
    assessment_service = AssessmentService(storage_client, settings)
    return assessment_service


@pytest.fixture
def assessment_service_multiple_choice_only(
        storage_client: Mock,
        settings: Mock,
        storage_files: StorageFiles
) -> AssessmentService:
    storage_client.list_files.side_effect = storage_files[:1] * 2
    assessment_service = AssessmentService(storage_client, settings)
    return assessment_service


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
