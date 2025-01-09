from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.database.exceptions import EntryNotFoundError
from app.database.tables.bucket_objects import DbBucketObjects
from app.repositories.utils import delete_entry, get_all
from tests.database.data_inserts import insert_bucket_object
from tests.database.utils import table_count


def test_get_all_without_filter(db_session: Session) -> None:
    for _ in range(10):
        insert_bucket_object(db_session)

    result = get_all(db_session, DbBucketObjects)

    assert len(result) == 10
    assert table_count(db_session, DbBucketObjects) == 10


def test_delete_entry_raises_exception_if_not_found(db_session: Session) -> None:
    with pytest.raises(EntryNotFoundError):
        delete_entry(db_session, DbBucketObjects, uuid4())
