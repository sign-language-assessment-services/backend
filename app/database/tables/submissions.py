from sqlalchemy import Column, Integer, JSON, String, Table

from app.database.metadata import metadata_obj

submissions = Table(
    "submissions",
    metadata_obj,
    Column("id", String, primary_key=True),
    Column("user_id", String, nullable=False),
    Column("assessment_id", String, nullable=False),
    Column("answers", JSON, nullable=False),
    Column("score", Integer, nullable=False)
)
