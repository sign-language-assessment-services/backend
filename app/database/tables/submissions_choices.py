from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.tables.base import Base


class SubmissionChoice(Base):
    __tablename__ = "submissions_choices"

    submission_id: Mapped[str] = mapped_column(
        ForeignKey("submissions.id"),
        primary_key=True
    )
    choice_id: Mapped[str] = mapped_column(
        ForeignKey("choices.id"),
        primary_key=True
    )
