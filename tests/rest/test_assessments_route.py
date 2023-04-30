from unittest.mock import Mock, patch

from fastapi.testclient import TestClient


@patch("app.core.interactors.assessments.get_presigned_url")
def test_get_assessment(get_presigned_url_mock: Mock, test_client: TestClient) -> None:
    get_presigned_url_mock.return_value = "http://data.localhost/slportal/witch.mp4"

    response = test_client.get("/assessments/1")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Elefantenprüfung",
        "items": [
            {
                "question": "Was essen Elefanten?",
                "choices":
                    [
                        {
                            "location": {
                                'bucket': "slportal",
                                'key': "hexen_algorithmus.mp4",
                            },
                            "is_correct": False,
                            "type": "video",
                            "url": "http://data.localhost/slportal/witch.mp4",
                        },
                        {
                            "location": {
                                'bucket': "slportal",
                                'key': "hexen_algorithmus.mp4",
                            },
                            "is_correct": True,
                            "type": "video",
                            "url": "http://data.localhost/slportal/witch.mp4",
                        },
                        {
                            "location": {
                                'bucket': "slportal",
                                'key': "hexen_algorithmus.mp4",
                            },
                            "is_correct": False,
                            "type": "video",
                            "url": "http://data.localhost/slportal/witch.mp4",
                        }
                    ]
            },
            {
                "question": "Was trinken Elefanten?",
                "choices":
                    [
                        {
                            "text": "Mineralwasser",
                            "is_correct": True,
                            "type": "text"
                        },
                        {
                            "text": "Limonade",
                            "is_correct": False,
                            "type": "text"
                        },
                        {
                            "text": "Wasser",
                            "is_correct": True,
                            "type": "text"
                        },
                        {
                            "text": "Hühnersuppe",
                            "is_correct": False,
                            "type": "text"
                        }
                    ]
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
