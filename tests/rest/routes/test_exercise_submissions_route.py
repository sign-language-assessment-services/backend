from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.rest.requests.exercise_submissions import UpsertExerciseSubmissionRequest
from app.rest.responses.exercise_submissions import UpsertExerciseSubmissionResponse
from tests.data.models.exercise_submissions import (
    exercise_submission_1, exercise_submission_2, exercise_submission_3, exercise_submission_4,
    exercise_submission_5, exercise_submission_6
)


def test_create_exercise_submission(test_client: TestClient) -> None:
    create_exercise_submission_request = jsonable_encoder(
        UpsertExerciseSubmissionRequest(
            answer=exercise_submission_1.answer.choices
        ),
        exclude_none=True
    )
    assessment_submission_id = str(exercise_submission_1.assessment_submission_id)
    exercise_id = str(exercise_submission_1.exercise_id)

    response = test_client.post(
        f"/assessment_submissions/{assessment_submission_id}/exercises/{exercise_id}/submissions/",
        json=create_exercise_submission_request
    ).json()

    create_exercise_submission_response = UpsertExerciseSubmissionResponse(**response)
    assert create_exercise_submission_response.id == exercise_submission_1.id


def test_get_exercise_submission(test_client: TestClient) -> None:
    submission_id = str(exercise_submission_1.id)

    response = test_client.get(f"/exercise_submissions/{submission_id}").json()

    assert response == {
        "id": str(exercise_submission_1.id),
        "assessment_submission_id": str(exercise_submission_1.assessment_submission_id),
        "exercise_id": str(exercise_submission_1.exercise_id),
        "answers": [str(choice_id) for choice_id in exercise_submission_1.answer.choices]
    }


def test_list_exercise_submissions(test_client: TestClient) -> None:
    response = test_client.get("/exercise_submissions/").json()

    assert response == [
        {
            "id": str(exercise_submission_1.id),
            "exercise_id": str(exercise_submission_1.exercise_id),
            "assessment_submission_id": str(exercise_submission_1.assessment_submission_id)
        },
        {
            "id": str(exercise_submission_2.id),
            "exercise_id": str(exercise_submission_2.exercise_id),
            "assessment_submission_id": str(exercise_submission_2.assessment_submission_id)

        },
        {
            "id": str(exercise_submission_3.id),
            "exercise_id": str(exercise_submission_3.exercise_id),
            "assessment_submission_id": str(exercise_submission_3.assessment_submission_id)
        },
        {
            "id": str(exercise_submission_4.id),
            "exercise_id": str(exercise_submission_4.exercise_id),
            "assessment_submission_id": str(exercise_submission_4.assessment_submission_id)
        },
        {
            "id": str(exercise_submission_5.id),
            "exercise_id": str(exercise_submission_5.exercise_id),
            "assessment_submission_id": str(exercise_submission_5.assessment_submission_id)

        },
        {
            "id": str(exercise_submission_6.id),
            "exercise_id": str(exercise_submission_6.exercise_id),
            "assessment_submission_id": str(exercise_submission_6.assessment_submission_id)
        }
    ]


def test_update_exercise_submission(test_client: TestClient) -> None:
    assessment_submission_id = str(exercise_submission_1.assessment_submission_id)
    exercise_id = str(exercise_submission_1.exercise_id)
    exercise_submission_response = test_client.post(
        f"/assessment_submissions/{assessment_submission_id}/exercises/{exercise_id}/submissions/",
        json={"answer": []}
    ).json()

    updated_exercise_submission_response = test_client.post(
        f"/assessment_submissions/{assessment_submission_id}/exercises/{exercise_id}/submissions/",
        params={"exercise_submission_id": exercise_submission_response["id"]},
        json={"answer": [str(choice) for choice in exercise_submission_1.answer.choices]}
    ).json()

    response_1 = UpsertExerciseSubmissionResponse(**exercise_submission_response)
    response_2 = UpsertExerciseSubmissionResponse(**updated_exercise_submission_response)
    assert response_1.id == response_2.id
