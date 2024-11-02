from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase


class DbMultipleChoice(DbBase):
    __tablename__ = "multiple_choices"

    # COLUMNS
    # ------------------------------------------------------------------------
    random: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    choices: Mapped[list["DbChoice"]] = relationship(
        back_populates="multiple_choice"
    )
    exercises: Mapped[list["DbExercise"]] = relationship(
        back_populates="multiple_choice"
    )
    multiple_choice_submissions: Mapped[list["DbMultipleChoiceSubmission"]] = relationship(
        back_populates="multiple_choice"
    )
