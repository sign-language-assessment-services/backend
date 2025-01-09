from unittest.mock import ANY

from fastapi.testclient import TestClient

from tests.data.models.submissions import (
    submission_1, submission_2, submission_3, submission_4, submission_5, submission_6
)


def test_add_submission(test_client: TestClient) -> None:
    assessment_id = str(submission_1.assessment_id)
    exercise_id = str(submission_1.exercise_id)

    response = test_client.post(
        f"/assessments/{assessment_id}/exercises/{exercise_id}/submissions/",
        json={"choices": [str(choice) for choice in submission_1.answer.choices]}
    ).json()

    assert response == {
        "id": ANY,
        "answers": [str(choice_id) for choice_id in submission_1.answer.choices],
        "assessment_id": str(submission_1.assessment_id),
        "exercise_id": str(submission_1.exercise_id),
        "multiple_choice_id": str(submission_1.multiple_choice_id),
        "user_id": str(submission_1.user_id)
    }
    assert isinstance(response["id"], str)


def test_get_submission(test_client: TestClient) -> None:
    submission_id = str(submission_1.id)

    response = test_client.get(f"/submissions/{submission_id}").json()

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
        },
        {
            "id": str(submission_3.id)
        },
        {
            "id": str(submission_4.id)
        },
        {
            "id": str(submission_5.id)
        },
        {
            "id": str(submission_6.id)
        },
    ]


def test_list_assessment_exercise_submissions_for_user(test_client: TestClient) -> None:
    assessment_id = str(submission_1.assessment_id)
    exercise_id = str(submission_1.exercise_id)

    response = test_client.get(
        f"/assessments/{assessment_id}/exercises/{exercise_id}/submissions/"
    ).json()

    assert response == [
        {
            "id": str(submission_1.id)
        },
        {
            "id": str(submission_2.id)
        }
    ]
