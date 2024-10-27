from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint

from app.database.tables.base import DbBase

submissions_choices = Table(
    "multiple_choice_submissions_choices",
    DbBase.metadata,

    # COLUMNS
    # ------------------------------------------------------------------------
    Column(
        "submission_id",
        ForeignKey("multiple_choice_submissions.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "choice_id",
        ForeignKey("choices.id", ondelete="CASCADE"),
        primary_key=True
    ),

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    UniqueConstraint("submission_id", "choice_id")
)
