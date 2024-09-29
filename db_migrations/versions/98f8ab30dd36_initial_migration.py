"""Initial migration

Revision ID: 98f8ab30dd36
Revises:
Create Date: 2024-09-29 18:56:55.464853+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "98f8ab30dd36"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assessments",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.Unicode(length=100),
            nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name"),
        )

    op.create_table(
        "multimedia_files",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "bucket",
            sa.String(length=63),
            nullable=False
        ),
        sa.Column(
            "key",
            sa.Unicode(length=1024),
            nullable=False
        ),
        sa.Column(
            "mediatype",
            sa.Enum(
                "IMAGE",
                "VIDEO",
                name="mediatype"
            ),
            nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "exercises",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
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
            "multimedia_file_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessments.id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["multimedia_file_id"],
            ["multimedia_files.id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "primers",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "position",
            sa.Integer(),
            nullable=False),
        sa.Column(
            "assessment_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "multimedia_file_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessments.id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["multimedia_file_id"],
            ["multimedia_files.id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "submissions",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.String(length=36),
            nullable=False
        ),
        sa.Column(
            "points",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "maximum_points",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "percentage",
            sa.Float(),
            nullable=False
        ),
        sa.Column(
            "assessment_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessments.id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "choices",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "is_correct",
            sa.Boolean(),
            nullable=False
        ),
        sa.Column(
            "exercise_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "multimedia_file_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["exercise_id"],
            ["exercises.id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["multimedia_file_id"],
            ["multimedia_files.id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "submissions_choices",
        sa.Column(
            "submission_id",
            sa.Uuid(),
            nullable=True
        ),
        sa.Column(
            "choice_id",
            sa.Uuid(),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["choice_id"],
            ["choices.id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["submission_id"],
            ["submissions.id"],
            ondelete="CASCADE"
        ),
    )


def downgrade() -> None:
    op.drop_table("submissions_choices")
    op.drop_table("choices")
    op.drop_table("submissions")
    op.drop_table("primers")
    op.drop_table("exercises")
    op.drop_table("multimedia_files")
    op.drop_table("assessments")
