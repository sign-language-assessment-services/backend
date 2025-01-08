from fastapi.testclient import TestClient

from tests.data.models.multimedia_files import multimedia_file_choice_1


def test_get_object_storage_url(test_client: TestClient) -> None:
    multimedia_file_id = str(multimedia_file_choice_1.id)

    response = test_client.get(f"/object-storage/{multimedia_file_id}").json()

    assert response == {
        "id": multimedia_file_id,
        "url": "http://some-url",
        "media_type": multimedia_file_choice_1.media_type.value
    }
