import pytest
from fastapi import status
from fastapi.testclient import TestClient


def test_get_assessment(test_client: TestClient) -> None:
    response = test_client.get("/assessments/1")

    assert response.json()["name"] == "Test Assessment"
    assert response.json()["items"] == [
        {
            "choices": [
                {
                    "is_correct": False,
                    "location": {
                        "bucket": "testbucket",
                        "key": "1-A.mp4"
                    },
                    "type": "video",
                    "url": ""
                },
                {
                    "is_correct": True,
                    "location": {
                        "bucket": "testbucket",
                        "key": "1-B.mp4"
                    },
                    "type": "video",
                    "url": ""
                }
            ],
            "position": 0,
            "question": {
                "location": {
                    "bucket": "testbucket",
                    "key": "question1.mp4"
                },
                "type": "video",
                "url": ""
            }
        },
        {
            "content": {
                "location": {
                    "bucket": "testbucket",
                    "key": "introduction.mp4"
                },
            "type": "video",
            "url": ""
            },
            "position": 0
        },
        {
            "choices": [
                {
                    "is_correct": True,
                    "location": {
                        "bucket": "testbucket",
                        "key": "2-A.mp4"
                    },
                    "type": "video",
               "url": ""
                },
                {
                    "is_correct": False,
                    "location": {
                        "bucket": "testbucket",
                        "key": "2-B.mp4"
                    },
                    "type": "video",
                    "url": ""
                },
                {
                    "is_correct": False,
                    "location": {
                        "bucket": "testbucket",
                        "key": "2-C.mp4"
                    },
                    "type": "video",
                    "url": ""
                }
            ],
            "position": 1,
            "question": {
                "location": {
                    "bucket": "testbucket",
                    "key": "question2.mp4"
                },
               "type": "video",
               "url": ""
            }
        }
    ]


def test_post_assessment(test_client: TestClient) -> None:
    assessment_id = 1
    submission = {
        0: [1],
        1: [0, 2]
    }

    response = test_client.post(
        f"/assessments/{assessment_id}/submissions/",
        json=submission
    )

    assert response.json() == {"score": 42}


def test_list_assessment(test_client: TestClient) -> None:
    response = test_client.get("/assessments/")

    assert response.json() == [
        {
            "id": "Test Assessment",
            "name": "Test Assessment"
        }
    ]


@pytest.mark.parametrize("endpoint", ["/assessments/", "/assessments/1"])
def test_get_allowed(test_client_allowed_roles: TestClient, endpoint: str) -> None:
    response = test_client_allowed_roles.get(endpoint)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("endpoint", ["/assessments/", "/assessments/1"])
def test_get_forbidden(test_client_no_roles: TestClient, endpoint: str) -> None:
    response = test_client_no_roles.get(endpoint)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("endpoint", ["/assessments/1/submissions/"])
def test_post_allowed(test_client_allowed_roles: TestClient, endpoint: str) -> None:
    response = test_client_allowed_roles.post(endpoint, json={0: [0, 1]})

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("endpoint", ["/assessments/1/submissions/"])
def test_post_forbidden(test_client_no_roles: TestClient, endpoint: str) -> None:
    response = test_client_no_roles.post(endpoint, json={0: [0, 1]})

    assert response.status_code == status.HTTP_403_FORBIDDEN
