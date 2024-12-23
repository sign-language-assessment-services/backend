from uuid import UUID

from sqlalchemy import Boolean, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, declared_attr, relationship

from app.database.tables.base import DbBase


class DbMultipleChoicesChoices(DbBase):
    __tablename__ = "multiple_choices_choices"

    @declared_attr
    def id(cls):
        return None

    @declared_attr
    def created_at(cls):
        return None

    # COLUMNS
    # ------------------------------------------------------------------------
    position: Mapped[int] = Column(
        Integer,
        nullable=False
    )
    is_correct: Mapped[bool] = Column(
        Boolean,
        nullable=False
    )

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    choice_id: Mapped[UUID] = Column(
        ForeignKey("choices.id", ondelete="CASCADE"),
        primary_key=True
    )
    multiple_choice_id: Mapped[UUID] = Column(
        ForeignKey("multiple_choices.id", ondelete="CASCADE"),
        primary_key=True
    )

    #  RELATIONSHIPS
    # ------------------------------------------------------------------------
    choice: Mapped["DbChoice"] = relationship(
        back_populates="associations",
        passive_deletes=True
    )
    multiple_choice: Mapped["DbMultipleChoice"] = relationship(
        back_populates="associations",
        passive_deletes=True
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    __table_args__ = (
        UniqueConstraint("multiple_choice_id", "position"),
    )
