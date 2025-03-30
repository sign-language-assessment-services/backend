from unittest.mock import ANY

from fastapi.testclient import TestClient

from tests.data.models.exercise_submissions import (
    exercise_submission_1, exercise_submission_2, exercise_submission_3, exercise_submission_4, exercise_submission_5,
    exercise_submission_6
)


def test_add_exercise_submission(test_client: TestClient) -> None:
    assessment_submission_id = str(exercise_submission_1.assessment_submission_id)
    exercise_id = str(exercise_submission_1.exercise_id)

    response = test_client.post(
        f"/assessment_submissions/{assessment_submission_id}/exercises/{exercise_id}/submissions/",
        json={"choices": [str(choice) for choice in exercise_submission_1.answer.choices]}
    ).json()

    assert response == {
        "id": ANY,
        "user_id": str(exercise_submission_1.user_id),
        "assessment_submission_id": str(exercise_submission_1.assessment_submission_id),
        "exercise_id": str(exercise_submission_1.exercise_id),
        "answers": [str(choice_id) for choice_id in exercise_submission_1.answer.choices]
    }
    assert isinstance(response["id"], str)


def test_get_exercise_submission(test_client: TestClient) -> None:
    submission_id = str(exercise_submission_1.id)

    response = test_client.get(f"/exercise_submissions/{submission_id}").json()

    assert response == {
        "id": str(exercise_submission_1.id),
        "user_id": str(exercise_submission_1.user_id),
        "assessment_submission_id": str(exercise_submission_1.assessment_submission_id),
        "exercise_id": str(exercise_submission_1.exercise_id),
        "answers": [str(choice_id) for choice_id in exercise_submission_1.answer.choices]
    }


def test_list_exercise_submissions(test_client: TestClient) -> None:
    response = test_client.get("/exercise_submissions/").json()

    assert response == [
        {
            "id": str(exercise_submission_1.id)
        },
        {
            "id": str(exercise_submission_2.id)
        },
        {
            "id": str(exercise_submission_3.id)
        },
        {
            "id": str(exercise_submission_4.id)
        },
        {
            "id": str(exercise_submission_5.id)
        },
        {
            "id": str(exercise_submission_6.id)
        },
    ]
