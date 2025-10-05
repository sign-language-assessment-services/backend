from unittest.mock import Mock

from app.external_services.minio.client import ObjectStorageClient
from tests.settings_for_tests import TestSettings


def test_fetch_access_token_posts_correct_payload_and_returns_json(monkeypatch) -> None:
    # Arrange
    settings = TestSettings()
    mocked_response = Mock()
    expected_json = {"access_token": "abc", "expires_in": 3600}
    mocked_response.json.return_value = expected_json

    mocked_post = Mock(return_value=mocked_response)

    # Patch requests.post used inside ObjectStorageClient
    monkeypatch.setattr(
        "app.external_services.minio.client.requests.post",
        mocked_post,
    )

    client = ObjectStorageClient(settings)

    # Act
    result = client._fetch_access_token()

    # Assert
    mocked_post.assert_called_once_with(
        url=settings.token_endpoint,
        data={
            "grant_type": "client_credentials",
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
        },
        timeout=10.0,
    )
    assert result == expected_json
