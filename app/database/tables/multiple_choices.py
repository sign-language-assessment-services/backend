from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase
from app.database.type_hints import Choices, Exercises


class DbMultipleChoice(DbBase):
    __tablename__ = "multiple_choice"

    # COLUMNS
    # ------------------------------------------------------------------------
    random: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    exercises: Mapped[Exercises] = relationship(
        back_populates="multiple_choice"
    )
    choices: Mapped[Choices] = relationship(
        back_populates="multiple_choice"
    )
