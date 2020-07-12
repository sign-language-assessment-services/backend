from test.base import get_test_client

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
            }
        ]
    }
