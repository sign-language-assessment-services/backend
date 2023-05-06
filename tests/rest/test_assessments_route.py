from unittest.mock import Mock, patch

from fastapi.testclient import TestClient


@patch("app.core.interactors.assessments.get_presigned_url")
def test_get_assessment(get_presigned_url_mock: Mock, test_client: TestClient) -> None:
    get_presigned_url_mock.return_value = "http://data.localhost/slportal/witch.mp4"

    response = test_client.get("/assessments/1")
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == "SLAS DSGS GV"
    assert len(json_response["items"]) == 7
    assert json_response["items"][0] == {
        "question": {
            "location": {
                "bucket": "slportal",
                "key": "slas_sgs_gv/exercises/1/01_Frage.mp4"
            },
            "url": "http://data.localhost/slportal/witch.mp4",
            "type": "video"
        },
        "choices": [
            {
                "location": {
                    "bucket": "slportal",
                    "key": "slas_sgs_gv/exercises/1/01a_Antwort.mp4"
                },
                "is_correct": False,
                "url": "http://data.localhost/slportal/witch.mp4",
                "type": "video"
            },
            {
                "location": {
                    "bucket": "slportal",
                    "key": "slas_sgs_gv/exercises/1/01b_Antwort.mp4"
                },
                "is_correct": True,
                "url": "http://data.localhost/slportal/witch.mp4",
                "type": "video"
            },
            {
                "location": {
                    "bucket": "slportal",
                    "key": "slas_sgs_gv/exercises/1/01c_Antwort.mp4"
                },
                "is_correct": False,
                "url": "http://data.localhost/slportal/witch.mp4",
                "type": "video"
            }
        ]
    }


@patch("app.rest.routers.assessments.score_assessment")
def test_post_assessment(score_asssessment_mock: Mock, test_client: TestClient) -> None:
    assessment_id = 1
    score_asssessment_mock.return_value = {"score": 2}
    submission = {
        0: [1],
        1: [0, 2]
    }

    response = test_client.post(
        f"/assessments/{assessment_id}/submissions/", json=submission
    )

    score_asssessment_mock.assert_called_once_with(assessment_id, submission)
    assert response.status_code == 200
    assert response.json() == {"score": 2}
