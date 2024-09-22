from sqlalchemy import Column, ForeignKey, Table, Uuid

from app.database.tables.base import Base

submission_choice_association = Table(
    "submissions_choices",
    Base.metadata,

    # COLUMNS
    # ------------------------------------------------------------------------
    Column(
        "submission_id",
        Uuid,
        ForeignKey(
            "submissions.id",
            ondelete="CASCADE"
        )
    ),
    Column(
        "choice_id",
        Uuid,
        ForeignKey(
            "choices.id",
            ondelete="CASCADE"
        )
    )
)
