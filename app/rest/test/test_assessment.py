from unittest.mock import patch

from .base import get_test_client

CLIENT = get_test_client()


def test_get_assessment():
    response = CLIENT.get("/assessments/1")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Elefantenprüfung",
        "items": [
            {
                "description": "Was essen Elefanten?",
                "choices":
                    [
                        {
                            "label": "Spaghetti Bolognese",
                            "is_correct": False
                        },
                        {
                            "label": "Nüsse",
                            "is_correct": True
                        },
                        {
                            "label": "Menschen",
                            "is_correct": False
                        }
                    ]
            },
            {
                "description": "Was trinken Elefanten?",
                "choices":
                    [
                        {
                            "label": "Mineralwasser",
                            "is_correct": True
                        },
                        {
                            "label": "Limonade",
                            "is_correct": False
                        },
                        {
                            "label": "Wasser",
                            "is_correct": True
                        },
                        {
                            "label": "Hühnersuppe",
                            "is_correct": False
                        }
                    ]
            }
        ]
    }


@patch("app.rest.routers.assessments.score_assessment")
def test_post_assessment(score_asssessment_mock):
    assessment_id = 1
    score_asssessment_mock.return_value = {"score": 2}
    submission = {
        0: [1],
        1: [0, 2]
    }

    response = CLIENT.post(
        f"/assessments/{assessment_id}/submissions/", json=submission
    )

    score_asssessment_mock.assert_called_once_with(assessment_id, submission)
    assert response.status_code == 200
    assert response.json() == {"score": 2}
