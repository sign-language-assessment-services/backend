from fastapi.testclient import TestClient

from tests.data.models.submissions import submission_1, submission_2


def test_get_submission(test_client: TestClient) -> None:
    submission_id = str(submission_1.id)

    response = test_client.get(f"/submissions/{submission_id}")
    response = response.json()

    assert response == {
        "id": str(submission_1.id),
        "answers": [str(choice_id) for choice_id in submission_1.answer.choices],
        "assessment_id": str(submission_1.assessment_id),
        "exercise_id": str(submission_1.exercise_id),
        "multiple_choice_id": str(submission_1.multiple_choice_id),
        "user_id": str(submission_1.user_id)
    }


def test_list_submissions(test_client: TestClient) -> None:
    response = test_client.get("/submissions/").json()

    assert response == [
        {
            "id": str(submission_1.id)
        },
        {
            "id": str(submission_2.id)
        }
    ]
