from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Table, UniqueConstraint

from app.database.metadata import metadata_obj

primers = Table(
    "primers",
    metadata_obj,
    Column("id", String(length=36), primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False),

    Column("position", Integer, nullable=False),

    Column("assessment_id", ForeignKey("assessments.id"), nullable=False),
    Column("multimedia_file_id", ForeignKey("multimedia_files.id"), nullable=False),

    UniqueConstraint("position", "assessment_id"),
)
