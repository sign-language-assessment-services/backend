from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy import text

from app.core.models.media_types import MediaType
from app.database.tables.multimedia_files import DbMultiMediaFile


@pytest.mark.parametrize(
    "mediatype_in,mediatype_out", [
        ("VIDEO", MediaType.VIDEO),
        ("IMAGE", MediaType.IMAGE)
    ]
)
def test_insert_valid_multimedia_file(mediatype_in, mediatype_out, db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket": "example_bucket",
        "key": "example_key",
        "mediatype": mediatype_in
    }

    _add_multimedia_file_data(db_session, **data)

    data_query = db_session.query(DbMultiMediaFile)
    assert data_query.count() == 1
    assert data_query.first().id == UUID(data.get("id"))
    assert data_query.first().created_at == data.get("created_at")
    assert data_query.first().bucket == data.get("bucket")
    assert data_query.first().key == data.get("key")
    assert data_query.first().mediatype == mediatype_out


def _add_multimedia_file_data(session, **kwargs) -> None:
    statement = text(
        """
        INSERT INTO multimedia_files(id, created_at, bucket, key, mediatype)
        VALUES (:id, :created_at, :bucket, :key, :mediatype)
        """
    )
    session.execute(statement, kwargs)
