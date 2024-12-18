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
                        "bucket_object": "testbucket",
                        "key": "1-A.mp4"
                    },
                    "type": "video",
                    "url": ""
                },
                {
                    "is_correct": True,
                    "location": {
                        "bucket_object": "testbucket",
                        "key": "1-B.mp4"
                    },
                    "type": "video",
                    "url": ""
                }
            ],
            "position": 0,
            "question": {
                "location": {
                    "bucket_object": "testbucket",
                    "key": "question1.mp4"
                },
                "type": "video",
                "url": ""
            }
        },
        {
            "content": {
                "location": {
                    "bucket_object": "testbucket",
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
                        "bucket_object": "testbucket",
                        "key": "2-A.mp4"
                    },
                    "type": "video",
               "url": ""
                },
                {
                    "is_correct": False,
                    "location": {
                        "bucket_object": "testbucket",
                        "key": "2-B.mp4"
                    },
                    "type": "video",
                    "url": ""
                },
                {
                    "is_correct": False,
                    "location": {
                        "bucket_object": "testbucket",
                        "key": "2-C.mp4"
                    },
                    "type": "video",
                    "url": ""
                }
            ],
            "position": 1,
            "question": {
                "location": {
                    "bucket_object": "testbucket",
                    "key": "question2.mp4"
                },
               "type": "video",
               "url": ""
            }
        }
    ]


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
    response = test_client_allowed_roles.post(endpoint, json={"0": {"choice-0": True, "choice-1": True}})

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("endpoint", ["/assessments/1/submissions/"])
def test_post_forbidden(test_client_no_roles: TestClient, endpoint: str) -> None:
    response = test_client_no_roles.post(endpoint, json={"0": {"choice-0": True, "choice-1": True}})

    assert response.status_code == status.HTTP_403_FORBIDDEN
