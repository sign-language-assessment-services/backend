from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.rest.requests.primers import CreatePrimerRequest
from tests.data.models.primers import primer_1, primer_2


def test_create_primer(test_client: TestClient) -> None:
    create_primer_request = jsonable_encoder(
        CreatePrimerRequest(
            multimedia_file_id=primer_1.content.id
        )
    )

    response = test_client.post("/primers/", json=create_primer_request).json()

    assert response == {
        "id": str(primer_1.id),
        "multimedia_file_id": str(primer_1.content.id)
    }


def test_get_primer(test_client: TestClient) -> None:
    primer_id = str(primer_1.id)

    response = test_client.get(f"/primers/{primer_id}")
    response = response.json()

    assert response == {
        "id": str(primer_1.id),
        "media_type": primer_1.content.media_type.value,
        "multimedia_file_id": str(primer_1.content.id)
    }


def test_list_primers(test_client: TestClient) -> None:
    response = test_client.get("/primers/").json()

    assert response == [
        {
            "id": str(primer_1.id),
            "media_type": primer_1.content.media_type.value,
        },
        {
            "id": str(primer_2.id),
            "media_type": primer_2.content.media_type.value,
        }
    ]
