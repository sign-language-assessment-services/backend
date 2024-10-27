"""Add initial secondary tables

Revision ID: 3c16ceb96151
Revises: 376f1b3cd3f1
Create Date: 2024-10-27 09:27:56.244103+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3c16ceb96151"
down_revision: Union[str, None] = "376f1b3cd3f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assessment_tasks",
        sa.Column(
            "position",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "assessment_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "task_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("assessment_id", "task_id"),
        sa.UniqueConstraint("assessment_id", "position")
    )
    op.create_table(
        "submissions_choices",
        sa.Column(
            "submission_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "choice_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(["choice_id"], ["choices.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["submission_id"], ["multiple_choice_submissions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("submission_id", "choice_id"),
        sa.UniqueConstraint("submission_id", "choice_id")
    )


def downgrade() -> None:
    op.drop_table("submissions_choices")
    op.drop_table("assessment_tasks")
