from sqlalchemy.orm import Mapped, relationship

from app.database.tables.base import DbBase
from app.database.tables.multiple_choices_choices import multiple_choices_choices


class DbMultipleChoice(DbBase):
    __tablename__ = "multiple_choices"

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    exercises: Mapped[list["DbExercise"]] = relationship(
        back_populates="multiple_choice"
    )
    choices: Mapped[list["DbChoice"]] = relationship(
        secondary=multiple_choices_choices,
        back_populates="multiple_choices"
    )
    submissions: Mapped[list["DbSubmission"]] = relationship(
        back_populates="multiple_choice"
    )
