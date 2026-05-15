"""add status enum to task

Revision ID: c7a2b3d4e5f6
Revises: b56bede8aa73
Create Date: 2026-05-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c7a2b3d4e5f6'
down_revision: Union[str, None] = 'b56bede8aa73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

task_status_enum = sa.Enum(
    'todo', 'in_progress', 'done', 'cancelled',
    name='taskstatus',
)

def upgrade() -> None:
    task_status_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        'task',
        sa.Column('status', task_status_enum, nullable=False, server_default='todo'),
    )
    op.create_index('ix_task_status', 'task', ['status'])


def downgrade() -> None:
    op.drop_index('ix_task_status', table_name='task')
    op.drop_column('task', 'status')
    task_status_enum.drop(op.get_bind(), checkfirst=True)