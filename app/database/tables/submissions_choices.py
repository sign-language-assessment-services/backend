from sqlalchemy import Column, ForeignKey, Table

from app.database.metadata import metadata_obj

submissions_choices = Table(
    "submissions_choices",
    metadata_obj,
    Column("submission_id", ForeignKey("submissions.id"), primary_key=True),
    Column("choice_id", ForeignKey("choices.id"), primary_key=True),
)
