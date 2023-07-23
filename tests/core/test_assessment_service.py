from typing import cast
from unittest.mock import Mock

import pytest

from app.config import Settings
from app.core.models.video_choice import VideoChoice
from app.core.models.video_question import VideoQuestion
from app.services.assessment_repository import AssessmentRepository
from app.services.assessment_service import AssessmentService
from app.services.object_storage_client import ObjectStorageClient


def test_get_assessment_by_id(
        object_storage_client: ObjectStorageClient,
        repository: Mock,
        settings: Settings
) -> None:
    assessment_service = AssessmentService(object_storage_client, repository, settings)
    assessment_id = 1

    assessment = assessment_service.get_assessment_by_id(assessment_id)

    repository.get_assessment_by_id.assert_called_once_with(assessment_id)
    assert assessment.name == "Test Assessment"
    for item in assessment.items:
        question = cast(VideoQuestion, item.question)
        assert question.url == "http://some-url"
        choices = cast(list[VideoChoice], item.choices)
        assert all((choice.url == "http://some-url" for choice in choices))


def test_exception_is_thrown_if_assessment_does_not_exist(
        object_storage_client: ObjectStorageClient,
        repository: Mock,
        settings: Settings
) -> None:
    assessment_service = AssessmentService(object_storage_client, repository, settings)
    repository.get_assessment_by_id.side_effect = KeyError('4711')

    with pytest.raises(KeyError, match="4711"):
        assessment_service.get_assessment_by_id(4711)


def test_score_assessment(
        object_storage_client: ObjectStorageClient,
        repository: AssessmentRepository,
        settings: Settings
) -> None:
    assessment_service = AssessmentService(object_storage_client, repository, settings)

    score = assessment_service.score_assessment(1, {0: [1], 1: [0]})

    assert score == {"score": 2}
