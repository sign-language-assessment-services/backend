from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase
from app.database.type_hints import Choices, Exercises, MultipleChoiceSubmissions


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
    choices: Mapped[Choices] = relationship(
        back_populates="multiple_choice"
    )
    exercises: Mapped[Exercises] = relationship(
        back_populates="multiple_choice"
    )
    multiple_choice_submissions: Mapped[MultipleChoiceSubmissions] = relationship(
        back_populates="multiple_choice"
    )
