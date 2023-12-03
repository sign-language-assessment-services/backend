from sqlalchemy import Column, String, TIMESTAMP, Table, Unicode, UniqueConstraint

from app.database.metadata import metadata_obj

multimedia_files = Table(
    "multimedia_files",
    metadata_obj,
    Column("id", String(length=36), primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False),

    Column("bucket", String(length=63), nullable=False),
    Column("key", Unicode(length=1024), nullable=False),

    UniqueConstraint("bucket", "key"),
)
