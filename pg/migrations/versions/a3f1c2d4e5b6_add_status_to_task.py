"""add status to task

Revision ID: a3f1c2d4e5b6
Revises: b56bede8aa73
Create Date: 2026-05-14 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3f1c2d4e5b6'
down_revision: Union[str, None] = 'b56bede8aa73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'task',
        sa.Column(
            'status',
            sa.String(length=32),
            nullable=False,
            server_default='todo',
        ),
    )
    op.create_index('ix_task_status', 'task', ['status'])


def downgrade() -> None:
    op.drop_index('ix_task_status', table_name='task')
    op.drop_column('task', 'status')
