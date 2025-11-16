from typing import Callable
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings

from app.core.models.assessment import Assessment
from app.core.models.assessment_submission import AssessmentSubmission
from app.core.models.choice import Choice
from app.core.models.exercise import Exercise
from app.core.models.exercise_submission import ExerciseSubmission
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.primer import Primer
from app.core.models.user import User
from app.database.orm import get_db_session
from app.external_services.minio.client import ObjectStorageClient
from app.main import app
from app.rest.dependencies import get_current_user
from app.rest.requests.assessment_submissions import UpdateAssessmentSubmissionToFinishedRequest
from app.services.assessment_service import AssessmentService
from app.services.assessment_submission_service import AssessmentSubmissionService
from app.services.choice_service import ChoiceService
from app.services.exceptions.not_found import (
    AssessmentNotFoundException, AssessmentSubmissionNotFoundException, ChoiceNotFoundException,
    ExerciseNotFoundException, ExerciseSubmissionNotFoundException, MultimediaFileNotFoundException,
    MultipleChoiceNotFoundException, PrimerNotFoundException, TaskNotFoundException
)
from app.services.exercise_service import ExerciseService
from app.services.exercise_submission_service import ExerciseSubmissionService
from app.services.multimedia_file_service import MultimediaFileService
from app.services.multiple_choice_service import MultipleChoiceService
from app.services.primer_service import PrimerService
from app.services.task_service import TaskService
from app.settings import get_settings
from tests.data.models.assessment_submissions import (
    assessment_submission_1, assessment_submission_1_updated, assessment_submission_2
)
from tests.data.models.assessments import assessment_1, assessment_2
from tests.data.models.choices import choice_1, choice_2, choice_3, choice_4
from tests.data.models.exercise_submissions import (
    exercise_submission_1, exercise_submission_2, exercise_submission_3, exercise_submission_4,
    exercise_submission_5, exercise_submission_6
)
from tests.data.models.exercises import exercise_1, exercise_2
from tests.data.models.multimedia_files import multimedia_file_choice_1, multimedia_file_choice_2
from tests.data.models.multiple_choices import multiple_choice_1, multiple_choice_2
from tests.data.models.primers import primer_1, primer_2
from tests.data.models.users import test_scorer_1, test_taker_1
from tests.settings_for_tests import TestSettings


@pytest.fixture
def app_dependency_overrides_data() -> FastAPI:
    app.dependency_overrides[get_current_user] = _get_override_current_user()
    app.dependency_overrides[get_db_session] = _get_override_db_session()
    app.dependency_overrides[get_settings] = _get_override_settings()

    app.dependency_overrides[AssessmentService] = _get_override_assessment_service(
        create_return=assessment_1,
        get_by_id_return=assessment_1,
        list_return=[assessment_1, assessment_2]
    )
    app.dependency_overrides[AssessmentSubmissionService] = _get_override_assessment_submission_service(
        create_return=assessment_submission_1,
        get_by_id_return=assessment_submission_1,
        update_submission=assessment_submission_1_updated,
        list_return=[assessment_submission_1, assessment_submission_2]
    )
    app.dependency_overrides[ChoiceService] = _get_override_choice_service(
        create_return=choice_1,
        get_by_id_return=choice_1,
        list_return=[choice_1, choice_2, choice_3, choice_4]
    )
    app.dependency_overrides[ExerciseService] = _get_override_exercise_service(
        create_return=exercise_1,
        get_by_id_return=exercise_1,
        list_return=[exercise_1, exercise_2]
    )
    app.dependency_overrides[MultimediaFileService] = _get_override_multimedia_file_service(
        create_return=multimedia_file_choice_1,
        get_by_id_return=multimedia_file_choice_1,
        list_return=[multimedia_file_choice_1, multimedia_file_choice_2]
    )
    app.dependency_overrides[MultipleChoiceService] = _get_override_multiple_choice_service(
        create_return=multiple_choice_1,
        get_by_id_return=multiple_choice_1,
        list_return=[multiple_choice_1, multiple_choice_2]
    )
    app.dependency_overrides[ObjectStorageClient] = _get_override_object_storage_client(
        get_presigned_url_return="http://some-url"
    )
    app.dependency_overrides[PrimerService] = _get_override_primer_service(
        create_return=primer_1,
        get_by_id_return=primer_1,
        list_return=[primer_1, primer_2]
    )
    app.dependency_overrides[ExerciseSubmissionService] = _get_override_exercise_submission_service(
        create_return=exercise_submission_1,
        get_by_id_return=exercise_submission_1,
        post_return=exercise_submission_1,
        list_return=[
            exercise_submission_1, exercise_submission_2, exercise_submission_3,
            exercise_submission_4, exercise_submission_5, exercise_submission_6
        ]
    )
    app.dependency_overrides[TaskService] = _get_override_task_service(
        get_by_id_return=[primer_1, exercise_1]
    )
    return app


@pytest.fixture
def app_dependency_overrides_no_data(app_dependency_overrides_data: FastAPI) -> FastAPI:
    app.dependency_overrides[AssessmentService] = _get_override_assessment_service()
    app.dependency_overrides[AssessmentSubmissionService] = _get_override_assessment_submission_service()
    app.dependency_overrides[ChoiceService] = _get_override_choice_service()
    app.dependency_overrides[ExerciseService] = _get_override_exercise_service()
    app.dependency_overrides[MultimediaFileService] = _get_override_multimedia_file_service()
    app.dependency_overrides[MultipleChoiceService] = _get_override_multiple_choice_service()
    app.dependency_overrides[ObjectStorageClient] = _get_override_object_storage_client()
    app.dependency_overrides[PrimerService] = _get_override_primer_service()
    app.dependency_overrides[ExerciseSubmissionService] = _get_override_exercise_submission_service()
    return app


@pytest.fixture
def test_client(app_dependency_overrides_data: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_client_with_scorer_role(app_dependency_overrides_data: FastAPI) -> TestClient:
    app.dependency_overrides[get_current_user] = _get_override_current_user(test_scorer_1)
    return TestClient(app)


@pytest.fixture
def test_client_not_found(app_dependency_overrides_no_data: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_client_no_roles(app_dependency_overrides_data: FastAPI) -> TestClient:
    app.dependency_overrides[get_current_user] = _get_override_current_user(User(id=test_taker_1.id, roles=[]))
    return TestClient(app)


def _get_override_settings(auth_enabled: bool = False) -> Callable:
    async def override_settings() -> BaseSettings:
        test_settings = TestSettings()
        test_settings.auth_enabled = auth_enabled
        return test_settings

    return override_settings


def _get_override_current_user(user: User = test_taker_1) -> Callable:
    async def override_get_current_user() -> User:
        return user

    return override_get_current_user


def _get_override_db_session() -> Callable:
    async def override_db_session() -> Mock:
        return Mock()

    return override_db_session


def _get_override_assessment_service(
        create_return: Assessment | None = None,
        get_by_id_return: Assessment | None = None,
        list_return: list[Assessment] | None = None
) -> Callable:
    async def override_assessment_service() -> Mock:
        assessment_service = Mock()
        assessment_service.create_assessment.return_value = create_return
        assessment_service.get_assessment_by_id.return_value = get_by_id_return
        assessment_service.list_assessments.return_value = list_return
        if get_by_id_return is None:
            assessment_service.get_assessment_by_id.side_effect = AssessmentNotFoundException()
        return assessment_service

    return override_assessment_service


def _get_override_assessment_submission_service(
        create_return: AssessmentSubmission | None = None,
        get_by_id_return: AssessmentSubmission | None = None,
        list_return: list[AssessmentSubmission] | None = None,
        update_submission: UpdateAssessmentSubmissionToFinishedRequest | None = None
) -> Callable:
    async def override_assessment_submission_service() -> Mock:
        assessment_submission_service = Mock()
        assessment_submission_service.create_assessment_submission.return_value = create_return
        assessment_submission_service.get_assessment_submission_by_id.return_value = get_by_id_return
        assessment_submission_service.list_assessment_submissions.return_value = list_return
        assessment_submission_service.update_assessment_submission.return_value = update_submission
        if get_by_id_return is None:
            assessment_submission_service.get_assessment_submission_by_id.side_effect = \
                AssessmentSubmissionNotFoundException()
        return assessment_submission_service

    return override_assessment_submission_service


def _get_override_choice_service(
        create_return: Choice | None = None,
        get_by_id_return: Choice | None = None,
        list_return: list[Choice] | None = None
):
    async def override_choice_service() -> Mock:
        choice_service = Mock()
        choice_service.create_choice.return_value = create_return
        choice_service.get_choice_by_id.return_value = get_by_id_return
        choice_service.list_choices.return_value = list_return
        if get_by_id_return is None:
            choice_service.get_choice_by_id.side_effect = ChoiceNotFoundException()
        return choice_service

    return override_choice_service


def _get_override_multiple_choice_service(
        create_return: MultipleChoice | None = None,
        get_by_id_return: MultipleChoice | None = None,
        list_return: list[MultipleChoice] | None = None
):
    async def override_choice_service() -> Mock:
        multiple_choice_service = Mock()
        multiple_choice_service.create_multiple_choice.return_value = create_return
        multiple_choice_service.get_multiple_choice_by_id.return_value = get_by_id_return
        multiple_choice_service.list_multiple_choices.return_value = list_return
        if get_by_id_return is None:
            multiple_choice_service.get_multiple_choice_by_id.side_effect = MultipleChoiceNotFoundException()
        return multiple_choice_service

    return override_choice_service


def _get_override_exercise_service(
        create_return: Exercise | None = None,
        get_by_id_return: Exercise | None = None,
        list_return: list[Exercise] | None = None
) -> Callable:
    async def override_exercise_service() -> Mock:
        exercise_service = Mock()
        exercise_service.create_exercise.return_value = create_return
        exercise_service.get_exercise_by_id.return_value = get_by_id_return
        exercise_service.list_exercises.return_value = list_return
        if get_by_id_return is None:
            exercise_service.get_exercise_by_id.side_effect = ExerciseNotFoundException()
        return exercise_service

    return override_exercise_service


def _get_override_multimedia_file_service(
        create_return: MultimediaFile | None = None,
        get_by_id_return: MultimediaFile | None = None,
        list_return: list[MultimediaFile] | None = None
) -> Callable:
    async def override_multimedia_file_service() -> Mock:
        multimedia_file_service = Mock()
        multimedia_file_service.create_multimedia_file.return_value = create_return
        multimedia_file_service.get_multimedia_file_by_id.return_value = get_by_id_return
        multimedia_file_service.list_multimedia_files.return_value = list_return
        if get_by_id_return is None:
            multimedia_file_service.get_multimedia_file_by_id.side_effect = MultimediaFileNotFoundException()
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
        create_return: Primer | None = None,
        get_by_id_return: Primer | None = None,
        list_return: list[Primer] | None = None
) -> Callable:
    async def override_primer_service() -> Mock:
        primer_service = Mock()
        primer_service.create_primer.return_value = create_return
        primer_service.get_primer_by_id.return_value = get_by_id_return
        primer_service.list_primers.return_value = list_return
        if get_by_id_return is None:
            primer_service.get_primer_by_id.side_effect = PrimerNotFoundException()
        return primer_service

    return override_primer_service


def _get_override_task_service(
        get_by_id_return: list[Primer | Exercise] | None = None
) -> Callable:
    async def override_task_service() -> Mock:
        task_service = Mock()
        task_service.get_task_by_id.side_effect = get_by_id_return
        if get_by_id_return is None:
            task_service.get_task_by_id.side_effect = TaskNotFoundException()
        return task_service

    return override_task_service


def _get_override_exercise_submission_service(
        create_return: ExerciseSubmission | None = None,
        get_by_id_return: ExerciseSubmission | None = None,
        post_return: ExerciseSubmission | None = None,
        list_return: list[ExerciseSubmission] | None = None,
) -> Callable:
    async def override_exercise_submission_service() -> Mock:
        submission_service = Mock()
        submission_service.create_exercise_submission.return_value = create_return
        submission_service.get_exercise_submission_by_id.return_value = get_by_id_return
        submission_service.list_exercise_submissions.return_value = list_return
        submission_service.upsert_exercise_submission.return_value = post_return
        if get_by_id_return is None:
            submission_service.get_exercise_submission_by_id.side_effect = ExerciseSubmissionNotFoundException()
        return submission_service

    return override_exercise_submission_service
