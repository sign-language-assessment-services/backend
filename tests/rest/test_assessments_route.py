from fastapi.testclient import TestClient


def test_get_assessment(test_client: TestClient) -> None:
    response = test_client.get("/assessments/1")
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == "Test Assessment"
    assert len(json_response["items"]) == 2
    assert json_response["items"][0] == {
        "position": 0,
        "choices": [
            {
                "is_correct": False,
                "location": {"bucket": "", "key": ""},
                "type": "video",
                "url": "http://1-A.mp4"
            },
            {
                "is_correct": True,
                "location": {"bucket": "", "key": ""},
                "type": "video",
                "url": "http://1-B.mp4"
            }
        ],
        "question": {
            "location": {"bucket": "", "key": ""},
            "type": "video",
            "url": "http://question1.mp4"
        }
    }


def test_post_assessment(test_client: TestClient) -> None:
    assessment_id = 1
    submission = {
        0: [1],
        1: [0, 2]
    }

    response = test_client.post(
        f"/assessments/{assessment_id}/submissions/", json=submission
    )

    assert response.status_code == 200
    assert response.json() == {"score": 42}
