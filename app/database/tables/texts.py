from sqlalchemy import UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase


class DbText(DbBase):
    __tablename__ = "texts"

    # COLUMNS
    # ------------------------------------------------------------------------
    text: Mapped[str] = mapped_column(
        UnicodeText,
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    choices: Mapped[list["DbChoice"]] = relationship(
        back_populates="text"
    )
    exercises: Mapped[list["DbExercise"]] = relationship(
        back_populates="text"
    )
    primers: Mapped[list["DbPrimer"]] = relationship(
        back_populates="text"
    )
