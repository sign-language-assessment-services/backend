from uuid import UUID

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase


class DbSubmission(DbBase):
    __tablename__ = "submissions"

    # COLUMNS
    # ------------------------------------------------------------------------
    user_name: Mapped[str] = mapped_column(
        String(length=36),
        nullable=False
    )
    choices: Mapped[list[UUID]] = mapped_column(
        MutableList.as_mutable(ARRAY(Uuid, dimensions=1)),
        nullable=True
    )

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    exercise_id: Mapped[UUID] = mapped_column(
        ForeignKey("exercises.id"),
        nullable=False
    )
    multiple_choice_id: Mapped[UUID] = mapped_column(
        ForeignKey("multiple_choices.id"),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    exercise: Mapped["DbExercise"] = relationship(
        back_populates="submissions"
    )
    multiple_choice: Mapped["DbMultipleChoice"] = relationship(
        back_populates="submissions"
    )
