from sqlalchemy import Boolean, Column, ForeignKey, String, TIMESTAMP, Table, UniqueConstraint

from app.database.metadata import metadata_obj

choices = Table(
    "choices",
    metadata_obj,
    Column("id", String(length=36), primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False),

    Column("is_correct", Boolean, nullable=False),

    Column("exercise_id", ForeignKey("exercises.id"), nullable=False),
    Column("multimedia_file_id", ForeignKey("multimedia_files.id"), nullable=False),

    UniqueConstraint("exercise_id", "multimedia_file_id"),
)
