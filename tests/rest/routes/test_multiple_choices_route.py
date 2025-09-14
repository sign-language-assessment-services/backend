from uuid import UUID

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.rest.requests.multiple_choices import CreateMultipleChoiceRequest
from app.rest.responses.multiple_choices import CreateMultipleChoiceResponse
from tests.data.models.multimedia_files import multimedia_file_choice_1, multimedia_file_choice_2
from tests.data.models.multiple_choices import multiple_choice_1, multiple_choice_2


def test_create_multiple_choices(test_client: TestClient) -> None:
    create_multiple_choice_request = jsonable_encoder(
        CreateMultipleChoiceRequest(
            choice_ids=[multimedia_file_choice_1.id, multimedia_file_choice_2.id],
            correct_choice_ids=[multimedia_file_choice_1.id]
        )
    )

    response = test_client.post("/multiple_choices/", json=create_multiple_choice_request).json()

    create_multiple_choice_response = CreateMultipleChoiceResponse(**response)
    assert isinstance(create_multiple_choice_response.id, UUID)


def test_get_multiple_choice(test_client: TestClient) -> None:
    multiple_choice_id = str(multiple_choice_1.id)

    response = test_client.get(f"/multiple_choices/{multiple_choice_id}").json()

    assert response.get("id") == multiple_choice_id


def test_list_multiple_choices(test_client: TestClient) -> None:
    response = test_client.get("/multiple_choices/").json()

    assert response == [
        {
            "id": str(multiple_choice_1.id),
            "number_of_choices": len(multiple_choice_1.choices)
        },
        {
            "id": str(multiple_choice_2.id),
            "number_of_choices": len(multiple_choice_2.choices)
        }
    ]
