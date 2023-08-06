# pylint: disable=redefined-outer-name

from unittest.mock import Mock

import pytest

from app.core.models.assessment import Assessment
from app.core.models.minio_location import MinioLocation
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.static_item import StaticItem
from app.core.models.video import Video
from app.core.models.video_choice import VideoChoice


@pytest.fixture
def multiple_choice_question1() -> MultipleChoice:
    return MultipleChoice(
        question=Video(location=MinioLocation(bucket="testbucket", key="question1.mp4")),
        choices=(
            VideoChoice(location=MinioLocation(bucket="testbucket", key="1-A.mp4"), is_correct=False),
            VideoChoice(location=MinioLocation(bucket="testbucket", key="1-B.mp4"), is_correct=True),
        )
    )


@pytest.fixture
def multiple_choice_question2() -> MultipleChoice:
    return MultipleChoice(
        question=Video(location=MinioLocation(bucket="testbucket", key="question2.mp4")),
        choices=(
            VideoChoice(location=MinioLocation(bucket="testbucket", key="2-A.mp4"), is_correct=True),
            VideoChoice(location=MinioLocation(bucket="testbucket", key="2-B.mp4"), is_correct=False),
            VideoChoice(location=MinioLocation(bucket="testbucket", key="2-C.mp4"), is_correct=False),
        )
    )


@pytest.fixture
def static_item() -> StaticItem:
    return StaticItem(
        Video(location=MinioLocation(bucket="testbucket", key="introduction.mp4"))
    )


@pytest.fixture(name="mocked_assessment")
def assessment(
        multiple_choice_question1: MultipleChoice,
        multiple_choice_question2: MultipleChoice,
        static_item: StaticItem
) -> Assessment:
    return Assessment(
        name="Test Assessment",
        items=(
            multiple_choice_question1,
            static_item,
            multiple_choice_question2
        )
    )


@pytest.fixture
def object_storage_client() -> Mock:
    object_storage_client = Mock()
    object_storage_client.get_presigned_url.return_value = "http://some-url"
    return object_storage_client


@pytest.fixture
def settings() -> Mock:
    settings = Mock()
    settings.data_bucket_name = "testbucket"
    return settings
