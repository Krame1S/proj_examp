"""create task tables in schemas

Revision ID: 709eeba87e07
Revises:
Create Date: 2026-05-28 11:32:11.073513
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "709eeba87e07"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "task",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("owner_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("todo", "in_progress", "done", "cancelled", name="taskstatus"),
            server_default="todo",
            nullable=False,
        ),
        # NO FK
        sa.Column("category_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="tasks",
    )

    op.create_index("ix_task_category_id", "task", ["category_id"], unique=False, schema="tasks")

    op.create_index("ix_task_owner_id", "task", ["owner_id"], unique=False, schema="tasks")

    op.create_table(
        "task_tag",
        sa.Column("task_id", sa.BigInteger(), nullable=False),
        # NO FK
        sa.Column("tag_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.task.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("task_id", "tag_id"),
        schema="tasks",
    )

    op.create_index("ix_task_tag_tag_id", "task_tag", ["tag_id"], unique=False, schema="tasks")

    op.create_index("ix_task_tag_task_id", "task_tag", ["task_id"], unique=False, schema="tasks")


def downgrade() -> None:
    op.drop_index("ix_task_tag_task_id", table_name="task_tag", schema="tasks")

    op.drop_index("ix_task_tag_tag_id", table_name="task_tag", schema="tasks")

    op.drop_table("task_tag", schema="tasks")

    op.drop_index("ix_task_owner_id", table_name="task", schema="tasks")

    op.drop_index("ix_task_category_id", table_name="task", schema="tasks")

    op.drop_table("task", schema="tasks")
