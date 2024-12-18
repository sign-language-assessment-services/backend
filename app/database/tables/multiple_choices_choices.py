from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table, UniqueConstraint

from app.database.tables.base import DbBase

multiple_choices_choices = Table(
    "multiple_choices_choices",
    DbBase.metadata,

    # COLUMNS
    # ------------------------------------------------------------------------
    Column(
        "position",
        Integer,
        nullable=False,
    ),
    Column(
        "is_correct",
        Boolean,
        nullable=False
    ),
    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    Column(
        "choice_id",
        ForeignKey("choices.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    ),
    Column(
        "multiple_choice_id",
        ForeignKey("multiple_choices.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    ),

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    UniqueConstraint("multiple_choice_id", "position")
)
