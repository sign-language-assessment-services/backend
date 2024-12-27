from unittest.mock import ANY
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND


def test_get_assessment(test_client: TestClient) -> None:
    response = test_client.get("/assessments/a0000000-0000-0000-0000-000000000001")

    assert response.json()["name"] == "Test Assessment 1"
    assert response.json()["tasks"] == [
        {
            # primer
            "id": ANY,
            "created_at": ANY,
            "content": {
                "id": ANY,
                "created_at": ANY,
                "location": {"bucket": "test", "key": "test.mpg"},
                "media_type": "VIDEO"
            }
        },
        {
            # exercise
            "id": ANY,
            "created_at": ANY,
            "points": 1,
            "question": {
                "content": {
                    "id": ANY,
                    "created_at": ANY,
                    "location": {"bucket": "test", "key": "test.mpg"},
                    "media_type": "VIDEO"
                }
            },
            "question_type": {
                # multiple choice
                "content": {
                    "id": ANY,
                    "created_at": ANY,
                    "choices": [
                        {
                            "id": ANY,
                            "created_at": ANY,
                            "is_correct": True,
                            "content": {
                                "id": ANY,
                                "created_at": ANY,
                                "location": {"bucket": "test", "key": "test.mpg"},
                                "media_type": "VIDEO"
                            }
                        },
                        {
                            "id": ANY,
                            "created_at": ANY,
                            "is_correct": False,
                            "content": {
                                "id": ANY,
                                "created_at": ANY,
                                "location": {"bucket": "test", "key": "test.mpg"},
                                "media_type": "VIDEO"
                            }
                        }
                    ]
                }
            }
        }
    ]


def test_get_assessment_not_found(test_client: TestClient) -> None:
    assessment_id = "ffffffff-eeee-dddd-cccc-bbbbbbbbbbbb"

    response = test_client.get(f"/assessments/{assessment_id}")
    assert response.status_code == HTTP_404_NOT_FOUND


def test_post_assessment(test_client: TestClient) -> None:
    assessment_id = "1"
    answers = {
        "0": {"choice-1": True},
        "1": {"choice-0": True, "choice-2": True}
    }

    response = test_client.post(
        f"/assessments/{assessment_id}/submissions/",
        json=answers
    )

    assert response.json() == {"points": 42, "maximum_points": 42, "percentage": 1}


def test_list_assessments(test_client: TestClient) -> None:
    response = test_client.get("/assessments/")

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == "a0000000-0000-0000-0000-000000000001"
    assert response.json()[0]["name"] == "Test Assessment 1"
    assert response.json()[1]["name"] == "Test Assessment 2"
    assert len(response.json()[0]["tasks"]) == 2
    assert len(response.json()[1]["tasks"]) == 2


@pytest.mark.parametrize("endpoint", ["/assessments/", f"/assessments/{uuid4()}"])
def test_get_allowed(test_client_allowed_roles: TestClient, endpoint: str) -> None:
    response = test_client_allowed_roles.get(endpoint)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("endpoint", ["/assessments/", f"/assessments/{uuid4()}"])
def test_get_forbidden(test_client_no_roles: TestClient, endpoint: str) -> None:
    response = test_client_no_roles.get(endpoint)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_allowed(test_client_allowed_roles: TestClient) -> None:
    endpoint = "/assessments/a0000000-0000-0000-0000-000000000001/submissions/"

    response = test_client_allowed_roles.post(endpoint, json={"0": {"choice-0": True, "choice-1": True}})

    assert response.status_code == status.HTTP_200_OK


def test_post_forbidden(test_client_no_roles: TestClient) -> None:
    endpoint = "/assessments/a0000000-0000-0000-0000-000000000001/submissions/"

    response = test_client_no_roles.post(endpoint, json={"0": {"choice-0": True, "choice-1": True}})

    assert response.status_code == status.HTTP_403_FORBIDDEN
