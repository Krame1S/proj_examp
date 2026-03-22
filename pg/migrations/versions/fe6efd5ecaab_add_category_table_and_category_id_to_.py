"""add category table and category_id to task

Revision ID: fe6efd5ecaab
Revises: 61d0f928eb6c
Create Date: 2026-03-22 17:58:10.956104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe6efd5ecaab'
down_revision: Union[str, None] = '61d0f928eb6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create category table
    op.create_table(
        'category',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_by', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='category_created_by_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='category_pkey'),
    )
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_index('ix_category_created_by', 'category', ['created_by'], unique=False)

    # Add category_id to task
    op.add_column('task', sa.Column('category_id', sa.BigInteger(), nullable=True))
    op.create_index(op.f('ix_task_category_id'), 'task', ['category_id'], unique=False)

    # Upgrade owner_id FK to have CASCADE (if not already)
    # First drop old FK
    op.drop_constraint('task_owner_id_fkey', 'task', type_='foreignkey')
    # Create new with CASCADE
    op.create_foreign_key(
        'task_owner_id_fkey',
        'task',
        'user',
        ['owner_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # Create new FK for category_id
    op.create_foreign_key(
        'task_category_id_fkey',
        'task',
        'category',
        ['category_id'],
        ['id'],
        ondelete='SET NULL'
    )

def downgrade() -> None:
    # Drop category FK
    op.drop_constraint('task_category_id_fkey', 'task', type_='foreignkey')

    # Drop owner_id FK
    op.drop_constraint('task_owner_id_fkey', 'task', type_='foreignkey')

    # Restore owner_id FK without CASCADE (adjust if your original had it)
    op.create_foreign_key(
        'task_owner_id_fkey',
        'task',
        'user',
        ['owner_id'],
        ['id']
    )

    op.drop_index(op.f('ix_task_category_id'), table_name='task')
    op.drop_column('task', 'category_id')

    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index('ix_category_created_by', table_name='category')
    op.drop_table('category')
