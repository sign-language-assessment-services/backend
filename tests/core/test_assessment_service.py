from unittest.mock import Mock

from app.config import Settings
from app.core.models.bucket_object import BucketObject
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia import Multimedia
from app.core.models.multimedia_choice import MultimediaChoice
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.static_item import StaticItem
from app.services.assessment_service import AssessmentService


def test_get_assessment_by_id(
        object_storage_client: Mock,
        settings: Settings
) -> None:
    object_storage_client.list_folders.return_value = ["00", "01"]
    object_storage_client.list_files.side_effect = [
        [
            BucketObject(
                name="frage",
                content_type="video/mp4"
            ),
            BucketObject(
                name="video_antwort",
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
    assessment_service = AssessmentService(object_storage_client, settings)
    assessment_id = "Test Assessment"

    assessment = assessment_service.get_assessment_by_id(assessment_id)

    assert assessment.name == "Test Assessment"

    assert assessment.items[0] == MultipleChoice(
        position=0,
        question=Multimedia(
            location=MinioLocation(
                bucket='testbucket',
                key='frage'
            ),
            url='http://some-url',
            type=MediaType.VIDEO
        ),
        choices=(
            MultimediaChoice(
                location=MinioLocation(
                    bucket='testbucket',
                    key='video_antwort'
                ),
                is_correct=False,
                url='http://some-url',
                type=MediaType.VIDEO
            ),
            MultimediaChoice(
                location=MinioLocation(
                    bucket='testbucket',
                    key='bild_antwort'
                ),
                is_correct=False,
                type=MediaType.IMAGE,
                url='http://some-url'
            )
        ),
    )

    assert assessment.items[1] == StaticItem(
        position=1,
        content=Multimedia(
            location=MinioLocation(
                bucket='testbucket',
                key='video'
            ),
            url='http://some-url',
            type=MediaType.VIDEO
        ),
    )


def test_score_assessment(
        object_storage_client: Mock,
        settings: Settings
) -> None:
    object_storage_client.list_folders.return_value = ["00", "01"]
    object_storage_client.list_files.return_value = [
        BucketObject(
            name="frage",
            content_type="video/mp4"
        ),
        BucketObject(
            name="antwort",
            content_type="video/mp4"
        ),
        BucketObject(
            name="antwort_richtig",
            content_type="video/mp4"
        ),
    ]
    assessment_service = AssessmentService(object_storage_client, settings)

    score = assessment_service.score_assessment("1", {0: [1], 1: [1]})

    assert score == {"score": 2}
