from datetime import UTC, datetime

from app.database.tables.multimedia_files import DbMultiMediaFile
from database.multimedia_files.test_add_multimedia_files import _add_multimedia_file_data


def test_delete_multimedia_file(db_session):
    data = {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket": "example_bucket",
        "key": "example_key",
        "content_type": "VIDEO"
    }
    _add_multimedia_file_data(db_session, **data)

    db_session.query(DbMultiMediaFile).delete()

    assert db_session.query(DbMultiMediaFile).count() == 0
