"""Delete user_id in exercise submissions

Revision ID: ec64a0fbdf2c
Revises: 6c37a4dce403
Create Date: 2025-06-28 08:56:23.813275+00:00
"""


from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# Revision identifiers used by Alembic
revision: str = "ec64a0fbdf2c"
down_revision: Union[str, None] = "6c37a4dce403"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("exercise_submissions", "user_id")


def downgrade() -> None:
    op.add_column(
        "exercise_submissions",
        sa.Column(
            "user_id",
            sa.UUID(),
            autoincrement=False,
            nullable=False
        )
    )
