from fastapi.testclient import TestClient

from tests.data.models.exercises import exercise_1, exercise_2


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
                "media_type": exercise_1.question_type.content.choices[0].content.media_type.value,
                "multimedia_file_id": str(exercise_1.question_type.content.choices[0].content.id),
            },
            {
                "id": str(exercise_1.question_type.content.choices[1].id),
                "media_type": exercise_1.question_type.content.choices[1].content.media_type.value,
                "multimedia_file_id": str(exercise_1.question_type.content.choices[1].content.id),
            },
            {
                "id": str(exercise_1.question_type.content.choices[2].id),
                "media_type": exercise_1.question_type.content.choices[2].content.media_type.value,
                "multimedia_file_id": str(exercise_1.question_type.content.choices[2].content.id),
            },
            {
                "id": str(exercise_1.question_type.content.choices[3].id),
                "media_type": exercise_1.question_type.content.choices[3].content.media_type.value,
                "multimedia_file_id": str(exercise_1.question_type.content.choices[3].content.id),
            }
        ]
    }


def test_list_exercises(test_client: TestClient) -> None:
    response = test_client.get("/exercises/").json()

    assert response == [
        {
            "id": str(exercise_1.id)
        },
        {
            "id": str(exercise_2.id)
        }
    ]
