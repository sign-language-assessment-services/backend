from unittest.mock import Mock

import pytest

from app.core.models.assessment import Assessment
from app.core.models.minio_location import MinioLocation
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.video_choice import VideoChoice
from app.core.models.video_question import VideoQuestion


@pytest.fixture(name="mocked_assessment")
def assessment() -> Assessment:
    return Assessment(
        name="Test Assessment",
        items=(
            MultipleChoice(
                question=VideoQuestion(location=MinioLocation(bucket="testbucket", key="question1.mp4")),
                choices=(
                    VideoChoice(location=MinioLocation(bucket="testbucket", key="1-A.mp4"), is_correct=False),
                    VideoChoice(location=MinioLocation(bucket="testbucket", key="1-B.mp4"), is_correct=True),
                )
            ),
            MultipleChoice(
                question=VideoQuestion(location=MinioLocation(bucket="testbucket", key="question2.mp4")),
                choices=(
                    VideoChoice(location=MinioLocation(bucket="testbucket", key="2-A.mp4"), is_correct=True),
                    VideoChoice(location=MinioLocation(bucket="testbucket", key="2-B.mp4"), is_correct=False),
                    VideoChoice(location=MinioLocation(bucket="testbucket", key="2-C.mp4"), is_correct=False),
                )
            )
        )
    )


@pytest.fixture
def object_storage_client() -> Mock:
    object_storage_client = Mock()
    object_storage_client.get_presigned_url.return_value = "http://some-url"
    return object_storage_client


@pytest.fixture
def repository(mocked_assessment: Assessment) -> Mock:
    repository = Mock()
    repository.get_assessment_by_id.return_value = mocked_assessment
    return repository


@pytest.fixture
def settings() -> Mock:
    settings = Mock()
    settings.data_bucket_name = "testbucket"
    return settings
