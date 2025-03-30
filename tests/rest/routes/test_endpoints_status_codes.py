from uuid import uuid4

import pytest
from fastapi import status
from starlette.testclient import TestClient

from tests.data.models.assessment_submissions import assessment_submission_1
from tests.data.models.assessments import assessment_1
from tests.data.models.exercise_submissions import exercise_submission_1
from tests.data.models.exercises import exercise_1
from tests.data.models.multimedia_files import multimedia_file_choice_1
from tests.data.models.primers import primer_1

GET_ENDPOINTS = [
    f"/assessment_submissions/{str(assessment_submission_1.id)}",
    f"/assessments/{str(assessment_1.id)}",
    f"/exercise_submissions/{str(exercise_submission_1.id)}",
    f"/exercises/{str(exercise_1.id)}",
    f"/object-storage/{str(multimedia_file_choice_1.id)}",
    f"/primers/{str(primer_1.id)}"
]


LIST_ENDPOINTS = [
    "/assessment_submissions/",
    "/assessments/",
    "/exercise_submissions/",
    "/exercises/",
    "/primers/",
]


@pytest.mark.parametrize("endpoint", GET_ENDPOINTS + LIST_ENDPOINTS)
def test_get_200(endpoint: str, test_client: TestClient) -> None:
    response = test_client.get(endpoint)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("endpoint", GET_ENDPOINTS + LIST_ENDPOINTS)
def test_get_403(endpoint: str, test_client_no_roles: TestClient) -> None:
    response = test_client_no_roles.get(endpoint)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("endpoint", GET_ENDPOINTS)
def test_get_not_found(endpoint: str, test_client_not_found: TestClient) -> None:
    response = test_client_not_found.get(endpoint)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_exercise_submission_200(test_client: TestClient) -> None:
    endpoint = f"/assessment_submissions/{str(assessment_submission_1.id)}/exercises/{str(exercise_1.id)}/submissions/"
    data = {"choices": [str(uuid4())]}

    response = test_client.post(endpoint, json=data)

    assert response.status_code == status.HTTP_200_OK


def test_post_exercise_submission_403(test_client_no_roles: TestClient) -> None:
    endpoint = f"/assessment_submissions/{str(assessment_submission_1.id)}/exercises/{str(exercise_1.id)}/submissions/"
    data = {"choices": [str(uuid4())]}

    response = test_client_no_roles.post(endpoint, json=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
