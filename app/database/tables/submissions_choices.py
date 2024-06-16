from sqlalchemy import Column, ForeignKey, Table

from app.database.tables.base import Base

submission_choice = Table(
    "submissions_choices",
    Base.metadata,
    Column("submission_id", ForeignKey("submissions.id")),
    Column("choice_id", ForeignKey("choices.id"))
)
