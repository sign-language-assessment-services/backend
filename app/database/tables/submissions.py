from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase
from app.database.type_hints import Exercise


class DbSubmission(DbBase):
    __tablename__ = "submissions"

    # COLUMNS
    # ------------------------------------------------------------------------
    user_name: Mapped[str] = mapped_column(
        String(length=36),
        nullable=False
    )
    exercise_id: Mapped[UUID] = mapped_column(
        ForeignKey("exercises.id"),
        nullable=False
    )
    submission_type: Mapped[str] = mapped_column(
        String(length=26),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    exercise: Mapped[Exercise] = relationship()

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_on": "submission_type",
        "polymorphic_identity": "submission"
    }
