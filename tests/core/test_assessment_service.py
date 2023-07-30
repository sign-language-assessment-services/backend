from typing import cast
from unittest.mock import Mock

from app.config import Settings
from app.core.models.video_choice import VideoChoice
from app.core.models.video_question import VideoQuestion
from app.services.assessment_service import AssessmentService


def test_get_assessment_by_id(
        object_storage_client: Mock,
        settings: Settings
) -> None:
    object_storage_client.list_folders.return_value = ["00", "01"]
    object_storage_client.list_files.return_value = ["frage", "antwort"]
    assessment_service = AssessmentService(object_storage_client, settings)
    assessment_id = "Test Assessment"

    assessment = assessment_service.get_assessment_by_id(assessment_id)

    assert assessment.name == "Test Assessment"
    for item in assessment.items:
        question = cast(VideoQuestion, item.question)
        assert question.url == "http://some-url"
        choices = cast(list[VideoChoice], item.choices)
        assert all((choice.url == "http://some-url" for choice in choices))


def test_score_assessment(
        object_storage_client: Mock,
        settings: Settings
) -> None:
    object_storage_client.list_folders.return_value = ["00", "01"]
    object_storage_client.list_files.return_value = ["frage", "antwort", "antwort_richtig"]
    assessment_service = AssessmentService(object_storage_client, settings)

    score = assessment_service.score_assessment("1", {0: [1], 1: [1]})

    assert score == {"score": 2}
