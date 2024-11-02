from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint

from app.database.tables.base import DbBase

assessments_tasks = Table(
    "assessments_tasks",
    DbBase.metadata,

    # COLUMNS
    # ------------------------------------------------------------------------
    Column(
        "position",
        Integer,
        nullable=False,
    ),

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    Column(
        "assessment_id",
        ForeignKey("assessments.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "task_id",
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True
    ),

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    UniqueConstraint("assessment_id", "position")
)
