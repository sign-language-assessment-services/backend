import pytest

from app.core.models.exceptions import UnsupportedMimeType
from app.core.models.media_types import MediaType


def test_image_mime_type() -> None:
    assert MediaType.from_content_type("image-01.jpeg") == MediaType.IMAGE


def test_video_mime_type() -> None:
    assert MediaType.from_content_type("video-01.mp4") == MediaType.VIDEO


def test_unsupported_mime_type() -> None:
    with pytest.raises(UnsupportedMimeType):
        MediaType.from_content_type("audio-01.mp3")
