from unittest.mock import Mock

import pytest

from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia import Multimedia
from app.core.models.multimedia_choice import MultimediaChoice
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.static_item import StaticItem


@pytest.fixture
def settings() -> Mock:
    settings = Mock()
    settings.data_endpoint = "127.0.0.1:4242"
    settings.data_bucket_name = "testbucket"
    settings.data_secure = False
    settings.data_sts_endpoint = "http://127.0.0.1:4242"
    return settings


@pytest.fixture
def multiple_choice_question1() -> MultipleChoice:
    return MultipleChoice(
        question=Multimedia(
            location=MinioLocation(bucket="testbucket", key="question1.mp4"),
            type=MediaType.VIDEO
        ),
        choices=(
            MultimediaChoice(
                location=MinioLocation(bucket="testbucket", key="1-A.mp4"),
                is_correct=False,
                type=MediaType.VIDEO
            ),
            MultimediaChoice(
                location=MinioLocation(bucket="testbucket", key="1-B.mp4"),
                is_correct=True,
                type=MediaType.VIDEO
            ),
        ),
        position=0
    )


@pytest.fixture
def multiple_choice_question2() -> MultipleChoice:
    return MultipleChoice(
        question=Multimedia(
            location=MinioLocation(bucket="testbucket", key="question2.mp4"),
            type=MediaType.VIDEO
        ),
        choices=(
            MultimediaChoice(
                location=MinioLocation(bucket="testbucket", key="2-A.mp4"),
                is_correct=True,
                type=MediaType.VIDEO
            ),
            MultimediaChoice(
                location=MinioLocation(bucket="testbucket", key="2-B.mp4"),
                is_correct=False,
                type=MediaType.VIDEO
            ),
            MultimediaChoice(
                location=MinioLocation(bucket="testbucket", key="2-C.mp4"),
                is_correct=False,
                type=MediaType.VIDEO
            ),
        ),
        position=1
    )


@pytest.fixture
def static_item() -> StaticItem:
    return StaticItem(
        position=0,
        content=Multimedia(
            location=MinioLocation(bucket="testbucket", key="introduction.mp4"),
            type=MediaType.VIDEO
        )
    )


@pytest.fixture
def assessment(
        multiple_choice_question1: MultipleChoice,
        multiple_choice_question2: MultipleChoice,
        static_item: StaticItem
) -> Assessment:
    return Assessment(
        name="Test Assessment",
        items=[
            multiple_choice_question1,
            static_item,
            multiple_choice_question2
        ]
    )


@pytest.fixture
def assessments() -> list[AssessmentSummary]:
    return [
        AssessmentSummary(
            id = "Test Assessment",
            name= "Test Assessment"
        )
    ]
