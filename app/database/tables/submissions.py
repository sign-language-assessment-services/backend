from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP, Table

from app.database.metadata import metadata_obj

submissions = Table(
    "submissions",
    metadata_obj,
    Column("id", String(length=36), primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False),

    Column("user_id", String(length=36), nullable=False),
    Column("points", Integer, nullable=False),
    Column("maximum_points", Integer, nullable=False),
    Column("percentage", Float, nullable=False),

    Column("assessment_id", ForeignKey("assessments.id"), nullable=False),
)
# TODO: 1. new database creation
#       2. alembic / make database migration possible (after other todos listed here)
#
# TODO: code changes to reflect db changes
#       1. Use submissions_choices n:m table instead of answers column JSON
#       2. Create mappings Domain models <-> Database models
