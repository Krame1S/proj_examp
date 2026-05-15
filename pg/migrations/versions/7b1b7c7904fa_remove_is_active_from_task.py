"""remove is_active from task

Revision ID: 7b1b7c7904fa
Revises: c7a2b3d4e5f6
Create Date: 2026-05-15 13:41:52.839614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b1b7c7904fa'
down_revision: Union[str, None] = 'c7a2b3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('task', 'is_active')

def downgrade() -> None:
    op.add_column('task', sa.Column('is_active', sa.BOOLEAN(), 
                  server_default=sa.text('true'), 
                  autoincrement=False, 
                  nullable=False))