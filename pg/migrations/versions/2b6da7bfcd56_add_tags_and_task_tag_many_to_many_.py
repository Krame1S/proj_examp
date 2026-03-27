"""add tags and task_tag many-to-many relationship
Revision ID: 2b6da7bfcd56
Revises: fe6efd5ecaab
Create Date: 2026-03-27 23:55:20.388683
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2b6da7bfcd56'
down_revision: Union[str, None] = 'fe6efd5ecaab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tag table
    op.create_table(
        'tag',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('created_by', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tag_name'), 'tag', ['name'], unique=True)
    op.create_index(op.f('ix_tag_created_by'), 'tag', ['created_by'], unique=False)

    # Create many-to-many table task_tag
    op.create_table(
        'task_tag',
        sa.Column('task_id', sa.BigInteger(), nullable=False),
        sa.Column('tag_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('task_id', 'tag_id')
    )
    op.create_index('ix_task_tag_task_id', 'task_tag', ['task_id'], unique=False)
    op.create_index('ix_task_tag_tag_id', 'task_tag', ['tag_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_task_tag_tag_id', table_name='task_tag')
    op.drop_index('ix_task_tag_task_id', table_name='task_tag')
    op.drop_table('task_tag')

    op.drop_index(op.f('ix_tag_name'), table_name='tag')
    op.drop_index(op.f('ix_tag_created_by'), table_name='tag')
    op.drop_table('tag')