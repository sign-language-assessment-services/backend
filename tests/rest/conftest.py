from typing import Callable
from unittest.mock import Mock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.choice import Choice
from app.core.models.exercise import Exercise
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.primer import Primer
from app.core.models.question import Question
from app.core.models.question_type import QuestionType
from app.core.models.user import User
from app.database.orm import get_db_session
from app.main import app
from app.rest.dependencies import get_current_user
from app.services.assessment_service import AssessmentService
from app.settings import get_settings


@pytest.fixture
def minio_location() -> MinioLocation:
    return MinioLocation(bucket="test", key="test.mpg")


@pytest.fixture
def multimedia_file(minio_location: MinioLocation) -> MultimediaFile:
    return MultimediaFile(location=minio_location, media_type=MediaType.VIDEO)


@pytest.fixture
def right_choice(multimedia_file: MultimediaFile) -> Choice:
    return Choice(content=multimedia_file, is_correct=True)


@pytest.fixture
def wrong_choice(multimedia_file: MultimediaFile) -> Choice:
    return Choice(content=multimedia_file, is_correct=False)


@pytest.fixture
def multiple_choice(right_choice: Choice, wrong_choice: Choice) -> MultipleChoice:
    return MultipleChoice(choices=[right_choice, wrong_choice])


@pytest.fixture
def question(multimedia_file: MultimediaFile) -> Question:
    return Question(content=multimedia_file)


@pytest.fixture
def question_type(multiple_choice: MultipleChoice) -> Question:
    return QuestionType(content=multiple_choice)


@pytest.fixture
def primer(multimedia_file: MultimediaFile) -> Primer:
    return Primer(content=multimedia_file)


@pytest.fixture
def exercise(question: Question, question_type: QuestionType) -> Exercise:
    return Exercise(points=1, question=question, question_type=question_type)


@pytest.fixture
def assessment_1(primer: Primer, exercise: Exercise) -> Assessment:
    return Assessment(
        id=UUID("a0000000-0000-0000-0000-000000000001"),
        name="Test Assessment 1",
        tasks=[primer, exercise]
    )


@pytest.fixture
def assessment_2(primer: Primer, exercise: Exercise) -> Assessment:
    return Assessment(name="Test Assessment 2", tasks=[primer, exercise])


@pytest.fixture
def assessments(assessment_1: Assessment, assessment_2: Assessment) -> list[Assessment]:
    return [assessment_1, assessment_2]


@pytest.fixture
def assessment_service(assessments: list[Assessment]) -> Mock:
    assessment_service = Mock()
    assessment_service.get_assessment_by_id.return_value = assessments[0]
    assessment_service.list_assessments.return_value = assessments
    return assessment_service


@pytest.fixture
def assessment_service_404() -> Mock:
    assessment_service = Mock()
    assessment_service.get_assessment_by_id.return_value = None
    return assessment_service


@pytest.fixture
def test_client(assessment_service: Mock) -> TestClient:
    app.dependency_overrides[AssessmentService] = lambda: assessment_service
    app.dependency_overrides[get_db_session] = _get_override_db_session()
    app.dependency_overrides[get_settings] = _get_override_settings(auth_enabled=False)
    return TestClient(app)


@pytest.fixture
def test_client_no_assessment(assessment_service_404: Mock) -> TestClient:
    app.dependency_overrides[AssessmentService] = lambda: assessment_service_404
    app.dependency_overrides[get_db_session] = _get_override_db_session()
    app.dependency_overrides[get_settings] = _get_override_settings(auth_enabled=False)
    return TestClient(app)


@pytest.fixture
def test_client_allowed_roles(assessment_service: Mock) -> TestClient:
    roles = ["slas-frontend-user", "test-taker"]
    app.dependency_overrides[get_current_user] = _get_override_current_user(roles=roles)
    app.dependency_overrides[get_db_session] = _get_override_db_session()
    app.dependency_overrides[AssessmentService] = lambda: assessment_service
    return TestClient(app)


@pytest.fixture
def test_client_no_roles(assessment_service: Mock) -> TestClient:
    app.dependency_overrides[get_settings] = _get_override_settings(auth_enabled=True)
    app.dependency_overrides[get_current_user] = _get_override_current_user(roles=[])
    app.dependency_overrides[AssessmentService] = lambda: assessment_service
    return TestClient(app)


def _get_override_settings(auth_enabled: bool = False) -> Callable:
    async def override_settings() -> Settings:
        return Settings(
            auth_enabled=auth_enabled,
            db_user="db_testuser",
            db_password="db_testpassword",
            db_host="db_testhost"
        )

    return override_settings


def _get_override_current_user(roles: list[str]) -> Callable:
    async def override_get_current_user() -> User:
        return User(
            id="testuser",
            roles=roles
        )

    return override_get_current_user


def _get_override_db_session() -> Callable:
    async def override_db_session() -> Mock:
        return Mock()

    return override_db_session
