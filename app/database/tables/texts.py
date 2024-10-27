from sqlalchemy import UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase
from app.database.type_hints import Choices, Exercises, Primers


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
    choices: Mapped[Choices] = relationship(
        back_populates="text"
    )
    exercises: Mapped[Exercises] = relationship(
        back_populates="text"
    )
    primers: Mapped[Primers] = relationship(
        back_populates="text"
    )
