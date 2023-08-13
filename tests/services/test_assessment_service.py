from unittest.mock import Mock

import pytest

from app.config import Settings
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.bucket_object import BucketObject
from app.core.models.exceptions import UnexpectedItemType
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia import Multimedia
from app.core.models.multimedia_choice import MultimediaChoice
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.static_item import StaticItem
from app.services.assessment_service import AssessmentService


def test_get_assessment_by_id(object_storage_client: Mock, settings: Settings) -> None:
    assessment_service = AssessmentService(object_storage_client, settings)
    assessment_id = "Test Assessment"

    assessment = assessment_service.get_assessment_by_id(assessment_id)

    assert assessment.name == "Test Assessment"
    assert assessment.items == (
        MultipleChoice(
            position=0,
            question=Multimedia(
                location=MinioLocation(
                    bucket="testbucket",
                    key="frage"
                ),
                url="http://some-url",
                type=MediaType.VIDEO
            ),
            choices=(
                MultimediaChoice(
                    location=MinioLocation(
                        bucket="testbucket",
                        key="video_antwort_richtig"
                    ),
                    is_correct=True,
                    url="http://some-url",
                    type=MediaType.VIDEO
                ),
                MultimediaChoice(
                    location=MinioLocation(
                        bucket="testbucket",
                        key="bild_antwort"
                    ),
                    is_correct=False,
                    type=MediaType.IMAGE,
                    url="http://some-url"
                )
            ),
        ),
        StaticItem(
            position=1,
            content=Multimedia(
                location=MinioLocation(
                    bucket="testbucket",
                    key="video"
                ),
                url="http://some-url",
                type=MediaType.VIDEO
            ),
        )
    )


def test_list_assessments(object_storage_client: Mock, settings: Settings) -> None:
    assessment_service = AssessmentService(object_storage_client, settings)

    assessments = assessment_service.list_assessments()

    assert assessments == [
        AssessmentSummary(id="00", name="00"),
        AssessmentSummary(id="01", name="01")
    ]


def test_score_assessment(
        object_storage_client: Mock,
        object_storage_files: list[list[BucketObject]],
        settings: Settings
) -> None:
    object_storage_client.list_files.side_effect = object_storage_files[:1] * 2
    assessment_service = AssessmentService(object_storage_client, settings)

    score = assessment_service.score_assessment("1", {0: [0], 1: [1]})

    assert score == {"score": 1}


def test_score_assessment_raises_exception_on_static_item(object_storage_client: Mock, settings: Settings) -> None:
    assessment_service = AssessmentService(object_storage_client, settings)

    with pytest.raises(UnexpectedItemType):
        assessment_service.score_assessment("1", {0: [0], 1: [1]})
