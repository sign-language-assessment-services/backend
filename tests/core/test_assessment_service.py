from unittest.mock import Mock

from app.config import Settings
from app.core.models.minio_location import MinioLocation
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.static_item import StaticItem
from app.core.models.video import Video
from app.core.models.video_choice import VideoChoice
from app.services.assessment_service import AssessmentService


def test_get_assessment_by_id(
        object_storage_client: Mock,
        settings: Settings
) -> None:
    object_storage_client.list_folders.return_value = ["00", "01"]
    object_storage_client.list_files.side_effect = [["frage", "antwort"], ["video"]]
    assessment_service = AssessmentService(object_storage_client, settings)
    assessment_id = "Test Assessment"

    assessment = assessment_service.get_assessment_by_id(assessment_id)

    assert assessment.name == "Test Assessment"

    assert assessment.items[0] == MultipleChoice(
        question=Video(
            location=MinioLocation(
                bucket='testbucket',
                key='frage'
            ),
            url='http://some-url',
            type='video'
        ),
        choices=(
            VideoChoice(
                location=MinioLocation(
                    bucket='testbucket',
                    key='antwort'
                ),
                is_correct=False,
                url='http://some-url',
                type='video'
            ),
        )
    )

    assert assessment.items[1] == StaticItem(
        Video(
            location=MinioLocation(
                bucket='testbucket',
                key='video'
            ),
            url='http://some-url',
            type='video'
        ),
    )


def test_score_assessment(
        object_storage_client: Mock,
        settings: Settings
) -> None:
    object_storage_client.list_folders.return_value = ["00", "01"]
    object_storage_client.list_files.return_value = [
        "frage", "antwort", "antwort_richtig"
    ]
    assessment_service = AssessmentService(object_storage_client, settings)

    score = assessment_service.score_assessment("1", {0: [1], 1: [1]})

    assert score == {"score": 2}
