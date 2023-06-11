from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.minio_location import MinioLocation
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.video_choice import VideoChoice
from app.core.models.video_question import VideoQuestion
from app.main import app
from app.rest.settings import get_settings
from app.services.assessment_service import AssessmentService


@pytest.fixture(name="mocked_assessment")
def assessment() -> Assessment:
    return Assessment(
        name="Test Assessment",
        items=(
            MultipleChoice(
                question=VideoQuestion(url="http://question1.mp4", location=MinioLocation(bucket="", key="")),
                choices=(
                    VideoChoice(url="http://1-A.mp4", is_correct=False, location=MinioLocation(bucket="", key="")),
                    VideoChoice(url="http://1-B.mp4", is_correct=True, location=MinioLocation(bucket="", key="")),
                )
            ),
            MultipleChoice(
                question=VideoQuestion(url="http://question2.mp4", location=MinioLocation(bucket="", key="")),
                choices=(
                    VideoChoice(url="http://2-A.mp4", is_correct=True, location=MinioLocation(bucket="", key="")),
                    VideoChoice(url="http://2-B.mp4", is_correct=False, location=MinioLocation(bucket="", key="")),
                    VideoChoice(url="http://2-C.mp4", is_correct=False, location=MinioLocation(bucket="", key="")),
                )
            )
        )
    )


@pytest.fixture
def mocked_assessment_service(mocked_assessment):
    assessment_service = Mock()
    assessment_service.get_assessment_by_id.return_value = mocked_assessment
    assessment_service.score_assessment.return_value = {"score": 42}
    return assessment_service


async def override_settings():
    settings = Settings()
    settings.auth_enabled = False
    return settings


@pytest.fixture
def test_client(mocked_assessment_service) -> TestClient:
    app.dependency_overrides[AssessmentService] = lambda: mocked_assessment_service
    app.dependency_overrides[get_settings] = override_settings

    return TestClient(app)
