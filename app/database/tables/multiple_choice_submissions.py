from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.multiple_choice_submissions_choices import submissions_choices
from app.database.tables.submissions import DbSubmission


class DbMultipleChoiceSubmission(DbSubmission):
    __tablename__ = "multiple_choice_submissions"

    # COLUMNS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        ForeignKey("submissions.id", ondelete="CASCADE"),
        primary_key=True
    )

    multiple_choice_id: Mapped[UUID] = mapped_column(
        ForeignKey("multiple_choices.id"),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    multiple_choice: Mapped["DbMultipleChoice"] = relationship(
        back_populates="multiple_choice_submissions"
    )

    choices: Mapped[list["DbChoice"]] = relationship(
        secondary=submissions_choices,
        back_populates="multiple_choice_submissions"
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_identity": "multiple_choice_submission"
    }
