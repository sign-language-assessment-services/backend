# pylint: disable=redefined-outer-name

from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia import Multimedia
from app.core.models.multimedia_choice import MultimediaChoice
from app.core.models.multiple_choice import MultipleChoice
from app.main import app
from app.rest.settings import get_settings
from app.services.assessment_service import AssessmentService


@pytest.fixture
def mocked_assessment() -> Assessment:
    return Assessment(
        name="Test Assessment",
        items=(
            MultipleChoice(
                position=0,
                question=Multimedia(
                    url="http://question1.mp4",
                    location=MinioLocation(bucket="", key=""),
                    type=MediaType.VIDEO
                ),
                choices=(
                    MultimediaChoice(
                        url="http://1-A.mp4",
                        is_correct=False,
                        location=MinioLocation(bucket="", key=""),
                        type=MediaType.VIDEO
                    ),
                    MultimediaChoice(
                        url="http://1-B.mp4",
                        is_correct=True,
                        location=MinioLocation(bucket="", key=""),
                        type=MediaType.VIDEO
                    ),
                )
            ),
            MultipleChoice(
                position=1,
                question=Multimedia(
                    url="http://question2.mp4",
                    location=MinioLocation(bucket="", key=""),
                    type=MediaType.VIDEO
                ),
                choices=(
                    MultimediaChoice(
                        url="http://2-A.mp4",
                        is_correct=True,
                        location=MinioLocation(bucket="", key=""),
                        type=MediaType.VIDEO
                    ),
                    MultimediaChoice(
                        url="http://2-B.mp4",
                        is_correct=False,
                        location=MinioLocation(bucket="", key=""),
                        type=MediaType.VIDEO
                    ),
                    MultimediaChoice(
                        url="http://2-C.mp4",
                        is_correct=False,
                        location=MinioLocation(bucket="", key=""),
                        type=MediaType.VIDEO
                    ),
                )
            )
        )
    )


@pytest.fixture
def mocked_assessment_service(mocked_assessment: Assessment) -> AssessmentService:
    assessment_service = Mock()
    assessment_service.get_assessment_by_id.return_value = mocked_assessment
    assessment_service.score_assessment.return_value = {"score": 42}
    return assessment_service


async def override_settings() -> Settings:
    settings = Settings()
    settings.auth_enabled = False
    return settings


@pytest.fixture
def test_client(mocked_assessment_service: AssessmentService) -> TestClient:
    app.dependency_overrides[AssessmentService] = lambda: mocked_assessment_service
    app.dependency_overrides[get_settings] = override_settings
    return TestClient(app)
