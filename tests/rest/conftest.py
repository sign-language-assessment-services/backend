from typing import Callable
from unittest.mock import Mock
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.exercise import Exercise
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.primer import Primer
from app.core.models.submission import Submission
from app.core.models.user import User
from app.database.orm import get_db_session
from app.main import app
from app.rest.dependencies import get_current_user
from app.services.assessment_service import AssessmentService
from app.services.exercise_service import ExerciseService
from app.services.multimedia_file_service import MultimediaFileService
from app.services.object_storage_client import ObjectStorageClient
from app.services.primer_service import PrimerService
from app.services.submission_service import SubmissionService
from app.settings import get_settings
from tests.data.models.assessments import assessment_1, assessment_2
from tests.data.models.exercises import exercise_1, exercise_2
from tests.data.models.multimedia_files import multimedia_file_choice_1, multimedia_file_choice_2
from tests.data.models.primers import primer_1, primer_2
from tests.data.models.submissions import (
    submission_1, submission_2, submission_3, submission_4, submission_5, submission_6
)
from tests.data.models.users import test_taker_1


@pytest.fixture
def app_dependency_overrides_data() -> FastAPI:
    app.dependency_overrides[get_current_user] = _get_override_current_user(
        user_id=test_taker_1.id,
        roles=test_taker_1.roles
    )
    app.dependency_overrides[get_db_session] = _get_override_db_session()
    app.dependency_overrides[get_settings] = _get_override_settings()

    app.dependency_overrides[AssessmentService] = _get_override_assessment_service(
        get_by_id_return=assessment_1,
        list_return=[assessment_1, assessment_2]
    )
    app.dependency_overrides[ExerciseService] = _get_override_exercise_service(
        get_by_id_return=exercise_1,
        list_return=[exercise_1, exercise_2]
    )
    app.dependency_overrides[MultimediaFileService] = _get_override_multimedia_file_service(
        get_by_id_return=multimedia_file_choice_1,
        list_return=[multimedia_file_choice_1, multimedia_file_choice_2]
    )
    app.dependency_overrides[ObjectStorageClient] = _get_override_object_storage_client(
        get_presigned_url_return="http://some-url"
    )
    app.dependency_overrides[PrimerService] = _get_override_primer_service(
        get_by_id_return=primer_1,
        list_return=[primer_1, primer_2]
    )
    app.dependency_overrides[SubmissionService] = _get_override_submission_service(
        get_by_id_return=submission_1,
        post_return=submission_1,
        list_return=[
            submission_1, submission_2, submission_3, submission_4, submission_5, submission_6
        ],
        list_user_exercise_return=[
            submission_1, submission_2
        ]
    )
    return app


@pytest.fixture
def app_dependency_overrides_no_data(app_dependency_overrides_data: FastAPI) -> FastAPI:
    app.dependency_overrides[AssessmentService] = _get_override_assessment_service()
    app.dependency_overrides[ExerciseService] = _get_override_exercise_service()
    app.dependency_overrides[MultimediaFileService] = _get_override_multimedia_file_service()
    app.dependency_overrides[ObjectStorageClient] = _get_override_object_storage_client()
    app.dependency_overrides[PrimerService] = _get_override_primer_service()
    app.dependency_overrides[SubmissionService] = _get_override_submission_service()
    return app


@pytest.fixture
def test_client(app_dependency_overrides_data: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_client_not_found(app_dependency_overrides_no_data: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_client_no_roles(app_dependency_overrides_no_data: FastAPI) -> TestClient:
    app.dependency_overrides[get_current_user] = _get_override_current_user(user_id=test_taker_1.id, roles=[])
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


def _get_override_current_user(user_id: UUID, roles: list[str]) -> Callable:
    async def override_get_current_user() -> User:
        return User(
            id=user_id,
            roles=roles
        )

    return override_get_current_user


def _get_override_db_session() -> Callable:
    async def override_db_session() -> Mock:
        return Mock()

    return override_db_session


def _get_override_assessment_service(
        get_by_id_return: Assessment | None = None,
        list_return: list[Assessment] | None = None
) -> Callable:
    async def override_assessment_service() -> Mock:
        assessment_service = Mock()
        assessment_service.get_assessment_by_id.return_value = get_by_id_return
        assessment_service.list_assessments.return_value = list_return
        return assessment_service

    return override_assessment_service


def _get_override_exercise_service(
        get_by_id_return: Exercise | None = None,
        list_return: list[Exercise] | None = None
) -> Callable:
    async def override_exercise_service() -> Mock:
        exercise_service = Mock()
        exercise_service.get_exercise_by_id.return_value = get_by_id_return
        exercise_service.list_exercises.return_value = list_return
        return exercise_service

    return override_exercise_service


def _get_override_multimedia_file_service(
        get_by_id_return: MultimediaFile | None = None,
        list_return: list[MultimediaFile] | None = None
) -> Callable:
    async def override_multimedia_file_service() -> Mock:
        multimedia_file_service = Mock()
        multimedia_file_service.get_multimedia_file_by_id.return_value = get_by_id_return
        multimedia_file_service.list_multimedia_files.return_value = list_return
        return multimedia_file_service

    return override_multimedia_file_service


def _get_override_object_storage_client(
        get_presigned_url_return: str | None = None
) -> Callable:
    async def override_object_storage_client() -> Mock:
        object_storage_client = Mock()
        object_storage_client.get_presigned_url.return_value = get_presigned_url_return
        return object_storage_client

    return override_object_storage_client


def _get_override_primer_service(
        get_by_id_return: Primer | None = None,
        list_return: list[Primer] | None = None
) -> Callable:
    async def override_primer_service() -> Mock:
        primer_service = Mock()
        primer_service.get_primer_by_id.return_value = get_by_id_return
        primer_service.list_primers.return_value = list_return
        return primer_service

    return override_primer_service


def _get_override_submission_service(
        get_by_id_return: Submission | None = None,
        post_return: Submission | None = None,
        list_return: list[Submission] | None = None,
        list_user_exercise_return: list[Submission] | None = None
) -> Callable:
    async def override_submission_service() -> Mock:
        submission_service = Mock()
        submission_service.get_submission_by_id.return_value = get_by_id_return
        submission_service.list_submissions.return_value = list_return
        submission_service.add_submission.return_value = post_return
        submission_service.get_all_submissions_for_assessment_and_user.return_value = list_user_exercise_return
        return submission_service

    return override_submission_service
