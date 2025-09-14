from fastapi.testclient import TestClient

from app.rest.requests.multimedia_files import CreateMultimediaFileRequest
from app.rest.responses.multimedia_files import (
    CreateMultimediaFileResponse, GetMultimediaFileResponse, ListMultimediaFileResponse
)
from tests.data.models.multimedia_files import multimedia_file_choice_1, multimedia_file_choice_2


def test_create_multimedia_file(test_client: TestClient, tmp_path) -> None:
    tmp_file = tmp_path / "test.mp4"
    tmp_file.write_bytes(b"test")
    create_multimedia_file_request = CreateMultimediaFileRequest(
        media_type=multimedia_file_choice_1.media_type
    )

    with open(tmp_file, "rb") as file:
        response = test_client.post(
            "/multimedia_files/",
            data={"meta_data": create_multimedia_file_request.model_dump_json()},
            files={"file": file}
        )
    response = response.json()

    create_multimedia_file_response = CreateMultimediaFileResponse(**response)
    assert create_multimedia_file_response.id == multimedia_file_choice_1.id
    assert create_multimedia_file_response.location.bucket == multimedia_file_choice_1.location.bucket
    assert create_multimedia_file_response.location.key == multimedia_file_choice_1.location.key


def test_get_multimedia_file(test_client: TestClient) -> None:
    multimedia_file_id = str(multimedia_file_choice_1.id)

    response = test_client.get(f"/multimedia_files/{multimedia_file_id}").json()

    get_multimedia_file_response = GetMultimediaFileResponse(**response)
    assert str(get_multimedia_file_response.id) == multimedia_file_id
    assert get_multimedia_file_response.url == multimedia_file_choice_1.url
    assert get_multimedia_file_response.media_type == multimedia_file_choice_1.media_type


def test_list_multimedia_files(test_client: TestClient) -> None:
    response = test_client.get("/multimedia_files/").json()

    list_response = [ListMultimediaFileResponse(**item) for item in response]

    assert list_response[0].id == multimedia_file_choice_1.id
    assert list_response[0].url == multimedia_file_choice_1.url
    assert list_response[0].media_type.value == multimedia_file_choice_1.media_type.value
    assert list_response[1].id == multimedia_file_choice_2.id
    assert list_response[1].url == multimedia_file_choice_2.url
    assert list_response[1].media_type.value == multimedia_file_choice_2.media_type.value
