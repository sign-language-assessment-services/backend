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


def test_get_assessment_not_found(test_client_no_assessment: TestClient) -> None:
    assessment_id = uuid4()

    response = test_client_no_assessment.get(f"/assessments/{assessment_id}")

    assert response.status_code == HTTP_404_NOT_FOUND


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
