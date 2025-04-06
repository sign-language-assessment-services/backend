from unittest.mock import ANY

from fastapi.testclient import TestClient

from tests.data.models.assessment_submissions import (
    assessment_submission_1, assessment_submission_2
)
from tests.data.models.users import test_taker_1


def test_add_assessment_submission(test_client: TestClient) -> None:
    assessment_id = str(assessment_submission_1.assessment_id)

    response = test_client.post(f"/assessments/{assessment_id}/submissions/").json()


    assert response == {"id": ANY}
    assert isinstance(response["id"], str)


def test_get_assessment_submission(test_client: TestClient) -> None:
    submission_id = assessment_submission_1.id

    response = test_client.get(f"/assessment_submissions/{submission_id}").json()

    assert response == {
        "id": str(submission_id),
        "user_id": str(test_taker_1.id),
        "assessment_id": str(assessment_submission_1.assessment_id),
        "score": None,
        "finished_at": None
    }


def test_list_assessment_submissions(test_client: TestClient) -> None:
    response = test_client.get("/assessment_submissions/").json()

    assert response == [
        {
            "id": str(assessment_submission_1.id)
        },
        {
            "id": str(assessment_submission_2.id)
        }
    ]
