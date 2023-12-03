from sqlalchemy import Column, String, TIMESTAMP, Table, Unicode

from app.database.metadata import metadata_obj

assessments = Table(
    "assessments",
    metadata_obj,
    Column("id", String(length=36), primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False),

    Column("name", Unicode(length=100), nullable=False, unique=True),
)
