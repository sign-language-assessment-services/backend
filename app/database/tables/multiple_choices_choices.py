from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

from app.database.tables.base import DbBase


class DbMultipleChoicesChoices(DbBase):
    __tablename__ = "multiple_choices_choices"

    @declared_attr
    def id(cls):  # pylint: disable=no-self-argument
        return None

    @declared_attr
    def created_at(cls):  # pylint: disable=no-self-argument
        return None

    # COLUMNS
    # ------------------------------------------------------------------------
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    choice_id: Mapped[UUID] = mapped_column(
        ForeignKey("choices.id", ondelete="CASCADE"),
        primary_key=True
    )
    multiple_choice_id: Mapped[UUID] = mapped_column(
        ForeignKey("multiple_choices.id", ondelete="CASCADE"),
        primary_key=True
    )

    #  RELATIONSHIPS
    # ------------------------------------------------------------------------
    choice: Mapped["DbChoice"] = relationship(
        back_populates="associations"
    )
    multiple_choice: Mapped["DbMultipleChoice"] = relationship(
        back_populates="associations"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    __table_args__ = (
        UniqueConstraint("multiple_choice_id", "position"),
    )
