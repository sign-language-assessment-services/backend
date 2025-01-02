from sqlalchemy.orm import Mapped, relationship

from app.database.tables.base import DbBase


class DbMultipleChoice(DbBase):
    __tablename__ = "multiple_choices"

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    exercises: Mapped[list["DbExercise"]] = relationship(
        back_populates="multiple_choice"
    )
    choices: Mapped[list["DbChoice"]] = relationship(
        secondary="multiple_choices_choices",
        back_populates="multiple_choices",
        viewonly=True
    )
    submissions: Mapped[list["DbSubmission"]] = relationship(
        back_populates="multiple_choice"
    )
    associations: Mapped[list["DbMultipleChoicesChoices"]] = relationship(
        back_populates="multiple_choice",
        passive_deletes=True
    )
