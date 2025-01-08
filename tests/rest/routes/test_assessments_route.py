from fastapi.testclient import TestClient

from tests.data.models.assessments import assessment_1, assessment_2


def test_get_assessment(test_client: TestClient) -> None:
    assessment_id = str(assessment_1.id)

    response = test_client.get(f"/assessments/{assessment_id}").json()

    assert response == {
        "id": assessment_id,
        "name": assessment_1.name,
        "tasks": [
            {
                "id": str(assessment_1.tasks[0].id),
                "task_type": "primer"
            },
            {
                "id": str(assessment_1.tasks[1].id),
                "task_type": "exercise"
            }
        ]
    }


def test_list_assessments(test_client: TestClient) -> None:
    response = test_client.get("/assessments/").json()

    assert response == [
        {
            "id": str(assessment_1.id),
            "name": assessment_1.name,
        },
        {
            "id": str(assessment_2.id),
            "name": assessment_2.name,
        }
    ]
