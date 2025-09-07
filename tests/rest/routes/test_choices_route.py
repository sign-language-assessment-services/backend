from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.rest.requests.choices import CreateChoiceRequest
from app.rest.responses.choices import CreateChoiceResponse
from tests.data.models.choices import choice_1, choice_2, choice_3, choice_4
from tests.data.models.multimedia_files import multimedia_file_choice_1


def test_create_choice(test_client: TestClient) -> None:
    create_choice_request = jsonable_encoder(CreateChoiceRequest(multimedia_file_id=multimedia_file_choice_1.id))

    response = test_client.post("/choices/", json=create_choice_request).json()

    create_choice_response = CreateChoiceResponse(**response)
    assert str(create_choice_response.id) == response["id"]


def test_get_choice(test_client: TestClient) -> None:
    choice_id = str(choice_1.id)

    response = test_client.get(f"/choices/{choice_id}").json()

    assert response == {
        "id": choice_id,
        "media_type": choice_1.content.media_type.value,
        "multimedia_file_id": str(choice_1.content.id),
        "multiple_choices": []
    }


def test_list_choices(test_client: TestClient) -> None:
    response = test_client.get("/choices/").json()

    assert response == [
        {
            "id": str(choice_1.id),
            "multimedia_file_id": str(choice_1.content.id),
            "media_type": choice_1.content.media_type.value,
        },
        {
            "id": str(choice_2.id),
            "multimedia_file_id": str(choice_2.content.id),
            "media_type": choice_2.content.media_type.value,
        },
        {
            "id": str(choice_3.id),
            "multimedia_file_id": str(choice_3.content.id),
            "media_type": choice_3.content.media_type.value,
        },
        {
            "id": str(choice_4.id),
            "multimedia_file_id": str(choice_4.content.id),
            "media_type": choice_4.content.media_type.value,
        }
    ]
