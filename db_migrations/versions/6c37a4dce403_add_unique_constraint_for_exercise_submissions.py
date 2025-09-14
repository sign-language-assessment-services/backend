"""Add unique constraint for exercise submissions

Revision ID: 6c37a4dce403
Revises: c7ae71fc77b5
Create Date: 2025-06-22 11:00:05.500951+00:00
"""

from typing import Sequence, Union

from alembic import op

# Revision identifiers used by Alembic
revision: str = "6c37a4dce403"
down_revision: Union[str, None] = "c7ae71fc77b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "exercise_submissions_assessment_submission_id_exercise_id_key",
        "exercise_submissions",
        ["assessment_submission_id", "exercise_id"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "exercise_submissions_assessment_submission_id_exercise_id_key",
        "exercise_submissions",
        type_="unique"
    )
