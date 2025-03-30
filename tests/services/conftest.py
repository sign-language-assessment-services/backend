from unittest.mock import Mock

import pytest
from minio.datatypes import Object as MinioObject

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.services.assessment_service import AssessmentService
from app.services.assessment_submission_service import AssessmentSubmissionService
from app.services.exercise_service import ExerciseService
from app.services.exercise_submission_service import ExerciseSubmissionService
from app.services.multimedia_file_service import MultimediaFileService
from app.services.object_storage_client import ObjectStorageClient
from app.services.primer_service import PrimerService


@pytest.fixture
def storage_folders() -> list[str]:
    return ["00", "01"]


@pytest.fixture
def storage_files() -> list[MultimediaFile]:
    return [
        MultimediaFile(
            location=MinioLocation(bucket="testbucket", key="00/question.mpg"),
            media_type=MediaType.VIDEO
        ),
        MultimediaFile(
            location=MinioLocation(bucket="testbucket", key="00/right_answer.mpg"),
            media_type=MediaType.VIDEO
        ),
        MultimediaFile(
            location=MinioLocation(bucket="testbucket", key="00/wrong_answer.mpg"),
            media_type=MediaType.IMAGE
        ),
        MultimediaFile(
            location=MinioLocation(bucket="testbucket", key="01/video.mpg"),
            media_type=MediaType.IMAGE
        )
    ]


@pytest.fixture
def storage_client(storage_files: list[MultimediaFile], storage_folders: list[str]) -> Mock:
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
    return AssessmentService(storage_client, settings)


@pytest.fixture
def exercise_service(settings: Mock) -> ExerciseService:
    return ExerciseService(settings)


@pytest.fixture
def multimedia_file_service(settings: Mock) -> MultimediaFileService:
    return MultimediaFileService(settings)


@pytest.fixture
def primer_service(settings: Mock) -> PrimerService:
    return PrimerService(settings)


@pytest.fixture
def exercise_submission_service(settings: Mock) -> ExerciseSubmissionService:
    return ExerciseSubmissionService(settings)


@pytest.fixture
def assessment_submission_service(settings: Mock) -> AssessmentSubmissionService:
    return AssessmentSubmissionService(settings)


@pytest.fixture
def assessment_service_multiple_choice_only(
        storage_client: Mock,
        settings: Mock,
        storage_files: list[MultimediaFile]
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
            metadata={"content-type": "VIDEO"}
        ),
        MinioObject(
            bucket_name="testbucket",
            object_name="file02",
            metadata={"content-type": "VIDEO"}
        )
    ]
