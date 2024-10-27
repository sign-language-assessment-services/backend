from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.submissions import DbSubmission
from app.database.type_hints import Choices, MultipleChoice


class DbMultipleChoiceSubmission(DbSubmission):
    __tablename__ = "multiple_choice_submissions"

    # COLUMNS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        ForeignKey("submissions.id", ondelete="CASCADE"),
        primary_key=True
    )
    multiple_choice_id: Mapped[UUID] = mapped_column(
        ForeignKey("multiple_choice.id"),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    multiple_choice: Mapped[MultipleChoice] = relationship()
    choices: Mapped[Choices] = relationship(
        secondary="submissions_choices",
        back_populates="submissions"
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_identity": "multiple_choice_submission"
    }
