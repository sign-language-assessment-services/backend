from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.rest.requests.exercises import CreateExerciseRequest
from app.rest.responses.exercises import CreateExerciseResponse
from tests.data.models.exercises import exercise_1, exercise_2
from tests.data.models.multimedia_files import multimedia_file_question_1
from tests.data.models.multiple_choices import multiple_choice_1


def test_create_exercise(test_client: TestClient) -> None:
    create_exercise_request = jsonable_encoder(
        CreateExerciseRequest(
            multimedia_file_id=multimedia_file_question_1.id,
            multiple_choice_id=multiple_choice_1.id
        )
    )

    response = test_client.post("/exercises/", json=create_exercise_request).json()

    create_exercise_response = CreateExerciseResponse(**response)
    assert create_exercise_response.id == exercise_1.id


def test_get_exercise(test_client: TestClient) -> None:
    exercise_id = str(exercise_1.id)

    response = test_client.get(f"/exercises/{exercise_id}")
    response = response.json()

    assert response == {
        "id": str(exercise_id),
        "points": exercise_1.points,
        "question": {
            "multimedia_file_id": str(exercise_1.question.content.id),
            "media_type": exercise_1.question.content.media_type.value,
        },
        "choices": [
            {
                "id": str(exercise_1.question_type.content.choices[0].id),
                "position": exercise_1.question_type.content.choices[0].position,
                "multimedia_file_id": str(exercise_1.question_type.content.choices[0].content.id),
                "media_type": exercise_1.question_type.content.choices[0].content.media_type.value
            },
            {
                "id": str(exercise_1.question_type.content.choices[1].id),
                "position": exercise_1.question_type.content.choices[1].position,
                "multimedia_file_id": str(exercise_1.question_type.content.choices[1].content.id),
                "media_type": exercise_1.question_type.content.choices[1].content.media_type.value
            },
            {
                "id": str(exercise_1.question_type.content.choices[2].id),
                "position": exercise_1.question_type.content.choices[2].position,
                "multimedia_file_id": str(exercise_1.question_type.content.choices[2].content.id),
                "media_type": exercise_1.question_type.content.choices[2].content.media_type.value
            },
            {
                "id": str(exercise_1.question_type.content.choices[3].id),
                "position": exercise_1.question_type.content.choices[3].position,
                "multimedia_file_id": str(exercise_1.question_type.content.choices[3].content.id),
                "media_type": exercise_1.question_type.content.choices[3].content.media_type.value
            }
        ]
    }


def test_list_exercises(test_client: TestClient) -> None:
    response = test_client.get("/exercises/").json()

    assert response == [
        {
            "id": str(exercise_1.id),
            "points": exercise_1.points
        },
        {
            "id": str(exercise_2.id),
            "points": exercise_2.points
        }
    ]
