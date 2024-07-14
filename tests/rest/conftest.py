from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.score import Score
from app.core.models.user import User
from app.database.orm import get_db_session
from app.main import app
from app.rest.dependencies import get_current_user
from app.services.assessment_service import AssessmentService
from app.settings import get_settings


@pytest.fixture
def assessment_service(assessment: Assessment, assessments: list[AssessmentSummary]) -> Mock:
    assessment_service = Mock()
    assessment_service.get_assessment_by_id.return_value = assessment
    assessment_service.list_assessments.return_value = assessments
    assessment_service.score_assessment.return_value = Score(points=42, maximum_points=42)
    return assessment_service


@pytest.fixture
def test_client(assessment_service: Mock) -> TestClient:
    async def override_settings() -> Settings:
        return Settings(
            auth_enabled=False,
            db_user="db_testuser",
            db_password="db_testpassword",
            db_host="db_testhost"
        )

    app.dependency_overrides[AssessmentService] = lambda: assessment_service
    app.dependency_overrides[get_db_session] = lambda: Mock()  # pylint: disable=unnecessary-lambda
    app.dependency_overrides[get_settings] = override_settings
    return TestClient(app)


@pytest.fixture
def test_client_allowed_roles(assessment_service: Mock) -> TestClient:
    async def overwrite_get_current_user() -> User:
        return User(
            id="testuser",
            roles=["slas-frontend-user", "test-taker"]
        )

    async def overwrite_settings() -> Settings:
        return Settings(
            auth_enabled=False,
            db_user="db_testuser",
            db_password="db_testpassword",
            db_host="db_testhost"
        )

    async def overwrite_db_session() -> Mock:
        return Mock()

    app.dependency_overrides[get_settings] = overwrite_settings
    app.dependency_overrides[get_current_user] = overwrite_get_current_user
    app.dependency_overrides[get_db_session] = overwrite_db_session
    app.dependency_overrides[AssessmentService] = lambda: assessment_service
    return TestClient(app)


@pytest.fixture
def test_client_no_roles(assessment_service: Mock) -> TestClient:
    async def overwrite_get_current_user() -> User:
        return User(
            id="testuser",
            roles=[]
        )

    async def overwrite_settings() -> Settings:
        return Settings(
            auth_enabled=True,
            db_user="db_testuser",
            db_password="db_testpassword",
            db_host="db_testhost"
        )

    app.dependency_overrides[get_settings] = overwrite_settings
    app.dependency_overrides[get_current_user] = overwrite_get_current_user
    app.dependency_overrides[AssessmentService] = lambda: assessment_service
    return TestClient(app)
