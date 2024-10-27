from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.tables.submissions import DbSubmission


class DbTextSubmission(DbSubmission):
    __tablename__ = "text_submissions"

    # COLUMNS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        ForeignKey("submissions.id", ondelete="CASCADE"),
        primary_key=True
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_identity": "text_submission"
    }
