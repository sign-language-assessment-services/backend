from unittest.mock import Mock

import pytest
from minio.datatypes import Object as MinioObject

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.external_services.minio.client import ObjectStorageClient
from app.services.assessment_service import AssessmentService
from app.services.assessment_submission_service import AssessmentSubmissionService
from app.services.choice_service import ChoiceService
from app.services.exercise_service import ExerciseService
from app.services.exercise_submission_service import ExerciseSubmissionService
from app.services.multimedia_file_service import MultimediaFileService
from app.services.multiple_choice_service import MultipleChoiceService
from app.services.primer_service import PrimerService
from app.services.scoring_service import ScoringService
from app.services.task_service import TaskService


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
def storage_client(storage_files: list[MultimediaFile]) -> Mock:
    object_storage_client = Mock()
    object_storage_client.get_presigned_url.return_value = "http://some-url"
    object_storage_client.list_files.side_effect = storage_files
    object_storage_client.list_folders.return_value = ["00", "01"]
    return object_storage_client


@pytest.fixture
def storage_client_minio(settings: Mock) -> ObjectStorageClient:
    object_storage_client = ObjectStorageClient(settings)
    object_storage_client.minio = Mock()
    return object_storage_client


@pytest.fixture
def multimedia_file_service(settings: Mock, storage_client: Mock) -> MultimediaFileService:
    return MultimediaFileService(settings, storage_client)


@pytest.fixture
def choice_service(settings: Mock, multimedia_file_service: MultimediaFileService) -> ChoiceService:
    return ChoiceService(settings, multimedia_file_service)


@pytest.fixture
def multiple_choice_service(settings: Mock, choice_service: ChoiceService) -> MultipleChoiceService:
    return MultipleChoiceService(settings, choice_service)


@pytest.fixture
def primer_service(settings: Mock, multimedia_file_service: MultimediaFileService) -> PrimerService:
    return PrimerService(settings, multimedia_file_service)


@pytest.fixture
def exercise_service(settings: Mock) -> ExerciseService:
    return ExerciseService(settings)


@pytest.fixture
def task_service(settings: Mock) -> TaskService:
    return TaskService()


@pytest.fixture
def assessment_service(settings: Mock, task_service: TaskService) -> AssessmentService:
    return AssessmentService(task_service)


@pytest.fixture
def scoring_service(settings: Mock) -> ScoringService:
    return ScoringService()


@pytest.fixture
def exercise_submission_service(settings: Mock, exercise_service: ExerciseService) -> ExerciseSubmissionService:
    return ExerciseSubmissionService(settings, ScoringService(), exercise_service)


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
