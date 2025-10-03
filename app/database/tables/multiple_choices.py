from sqlalchemy.orm import Mapped, relationship

from app.database.tables.base import DbBase


class DbMultipleChoice(DbBase):
    __tablename__ = "multiple_choices"

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    exercises: Mapped[list["DbExercise"]] = relationship(
        back_populates="multiple_choice",
        lazy="selectin"
    )
    choices: Mapped[list["DbChoice"]] = relationship(
        secondary="multiple_choices_choices",
        back_populates="multiple_choices",
        viewonly=True,
        lazy="selectin"
    )
    associations: Mapped[list["DbMultipleChoicesChoices"]] = relationship(
        back_populates="multiple_choice",
        passive_deletes=True,
        lazy="selectin"
    )
