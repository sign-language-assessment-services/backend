from sqlalchemy import JSON, TIMESTAMP, Column, Float, Integer, String, Table

from app.database.metadata import metadata_obj

submissions = Table(
    "submissions",
    metadata_obj,
    Column("id", String, primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False),
    Column("user_id", String, nullable=False),
    Column("assessment_id", String, nullable=False),
    Column("answers", JSON, nullable=False),
    Column("points", Integer, nullable=False),
    Column("maximum_points", Integer, nullable=False),
    Column("percentage", Float, nullable=False)
)
