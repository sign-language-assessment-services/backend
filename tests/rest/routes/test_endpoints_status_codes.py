from pathlib import Path
from uuid import uuid4

import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.rest.requests.assessments import CreateAssessmentRequest
from app.rest.requests.multimedia_files import CreateMultimediaFileRequest
from tests.data.models.assessment_submissions import assessment_submission_1
from tests.data.models.assessments import assessment_1
from tests.data.models.choices import associated_choice_1, associated_choice_2
from tests.data.models.exercise_submissions import exercise_submission_1
from tests.data.models.exercises import exercise_1
from tests.data.models.multimedia_files import multimedia_file_choice_1
from tests.data.models.multiple_choices import multiple_choice_1
from tests.data.models.primers import primer_1

GET_ENDPOINTS = [
    f"/assessment_submissions/{str(assessment_submission_1.id)}",
    f"/assessments/{str(assessment_1.id)}",
    f"/choices/{str(associated_choice_1.id)}",
    f"/exercise_submissions/{str(exercise_submission_1.id)}",
    f"/exercises/{str(exercise_1.id)}",
    f"/multimedia_files/{str(multimedia_file_choice_1.id)}",
    f"/multiple_choices/{str(multiple_choice_1.id)}",
    f"/primers/{str(primer_1.id)}"
]
LIST_ENDPOINTS = [
    "/assessment_submissions/",
    "/assessments/",
    "/choices/",
    "/exercise_submissions/",
    "/exercises/",
    "/multimedia_files/",
    "/multiple_choices/",
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
def test_get_404(endpoint: str, test_client_not_found: TestClient) -> None:
    response = test_client_not_found.get(endpoint)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_assessment_200(test_client: TestClient) -> None:
    create_assessment_request = CreateAssessmentRequest(name=assessment_1.name).model_dump()

    response = test_client.post("/assessments/", json=create_assessment_request)

    assert response.status_code == status.HTTP_200_OK


def test_post_assessment_403(test_client_no_roles: TestClient) -> None:
    create_assessment_request = CreateAssessmentRequest(name=assessment_1.name).model_dump()

    response = test_client_no_roles.post("/assessments/", json=create_assessment_request)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_assessment_submission_200(test_client: TestClient) -> None:
    endpoint = f"/assessments/{str(assessment_1.id)}/submissions/"

    response = test_client.post(endpoint)

    assert response.status_code == status.HTTP_200_OK


def test_post_assessment_submission_403(test_client_no_roles: TestClient) -> None:
    endpoint = f"/assessments/{str(assessment_1.id)}/submissions/"

    response = test_client_no_roles.post(endpoint)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_put_assessment_submission_200(test_client: TestClient) -> None:
    endpoint = f"/assessment_submissions/{str(assessment_submission_1.id)}"

    response = test_client.put(endpoint, json={"finished": True})

    assert response.status_code == status.HTTP_200_OK


def test_put_assessment_submission_403(test_client_no_roles: TestClient) -> None:
    endpoint = f"/assessment_submissions/{str(assessment_submission_1.id)}"

    response = test_client_no_roles.put(endpoint, json={"finished": True})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_put_assessment_submission_404(test_client_not_found: TestClient) -> None:
    endpoint = f"/assessment_submissions/{str(uuid4())}"

    response = test_client_not_found.put(endpoint, json={"finished": True})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_choice_200(test_client: TestClient) -> None:
    endpoint = f"/choices/"
    data = {"multimedia_file_id": str(multimedia_file_choice_1.id)}

    response = test_client.post(endpoint, json=data)

    assert response.status_code == status.HTTP_200_OK


def test_post_choice_403(test_client_no_roles: TestClient) -> None:
    endpoint = f"/choices/"
    data = {"multimedia_file_id": str(multimedia_file_choice_1.id)}

    response = test_client_no_roles.post(endpoint, json=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_exercise_200(test_client: TestClient) -> None:
    endpoint = f"/exercises/"
    data = {
        "multimedia_file_id": str(multimedia_file_choice_1.id),
        "multiple_choice_id": str(multiple_choice_1.id)
    }

    response = test_client.post(endpoint, json=data)

    assert response.status_code == status.HTTP_200_OK


def test_post_exercise_403(test_client_no_roles: TestClient) -> None:
    endpoint = f"/exercises/"
    data = {
        "multimedia_file_id": str(multimedia_file_choice_1.id),
        "multiple_choice_id": str(multiple_choice_1.id)
    }

    response = test_client_no_roles.post(endpoint, json=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_exercise_submission_200(test_client: TestClient) -> None:
    endpoint = f"/assessment_submissions/{str(assessment_submission_1.id)}/exercises/{str(exercise_1.id)}/submissions/"
    data = {"answer": [str(uuid4())]}

    response = test_client.post(endpoint, json=data)

    assert response.status_code == status.HTTP_200_OK


def test_post_exercise_submission_403(test_client_no_roles: TestClient) -> None:
    endpoint = f"/assessment_submissions/{str(assessment_submission_1.id)}/exercises/{str(exercise_1.id)}/submissions/"
    data = {"answer": [str(uuid4())]}

    response = test_client_no_roles.post(endpoint, json=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_multimedia_file_200(test_client: TestClient, tmp_path: Path) -> None:
    tmp_file = tmp_path / "test.mp4"
    tmp_file.write_bytes(b"test")
    create_multimedia_file_request = CreateMultimediaFileRequest(
        media_type=multimedia_file_choice_1.media_type
    )
    endpoint = "/multimedia_files/"
    data = {"meta_data": create_multimedia_file_request.model_dump_json()}

    with open(tmp_file, "rb") as file:
        response = test_client.post(endpoint, data=data, files={"file": file})

    assert response.status_code == status.HTTP_200_OK


def test_post_multimedia_file_403(test_client_no_roles: TestClient, tmp_path: Path) -> None:
    tmp_file = tmp_path / "test.mp4"
    tmp_file.write_bytes(b"test")
    create_multimedia_file_request = CreateMultimediaFileRequest(
        media_type=multimedia_file_choice_1.media_type
    )
    endpoint = "/multimedia_files/"
    data = {"meta_data": create_multimedia_file_request.model_dump_json()}

    with open(tmp_file, "rb") as file:
        response = test_client_no_roles.post(endpoint, data=data, files={"file": file})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_multiple_choice_200(test_client: TestClient) -> None:
    endpoint = "/multiple_choices/"
    data = {
        "choice_ids": [str(associated_choice_1.id), str(associated_choice_2.id)],
        "correct_choice_ids": [str(associated_choice_1.id)]
    }

    response = test_client.post(endpoint, json=data)

    assert response.status_code == status.HTTP_200_OK


def test_post_multiple_choice_403(test_client_no_roles: TestClient) -> None:
    endpoint = "/multiple_choices/"
    data = {
        "choice_ids": [str(associated_choice_1.id), str(associated_choice_2.id)],
        "correct_choice_ids": [str(associated_choice_1.id)]
    }

    response = test_client_no_roles.post(endpoint, json=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_multiple_choice_422(test_client: TestClient) -> None:
    endpoint = "/multiple_choices/"
    data = {
        "choice_ids": [str(associated_choice_1.id), str(associated_choice_2.id)],
        "correct_choice_ids": [str(uuid4())]  # not subset of choice_ids
    }

    response = test_client.post(endpoint, json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "correct choices have to be a subset of choices" in response.text


def test_post_primer_200(test_client: TestClient) -> None:
    endpoint = "/primers/"
    data = {"multimedia_file_id": str(multimedia_file_choice_1.id)}

    response = test_client.post(endpoint, json=data)

    assert response.status_code == status.HTTP_200_OK


def test_post_primer_403(test_client_no_roles: TestClient) -> None:
    endpoint = "/primers/"
    data = {"multimedia_file_id": str(multimedia_file_choice_1.id)}

    response = test_client_no_roles.post(endpoint, json=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
