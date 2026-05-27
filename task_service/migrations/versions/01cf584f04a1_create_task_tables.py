"""create task tables

Revision ID: 01cf584f04a1
Revises: 
Create Date: 2026-05-27 16:07:54.233344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '01cf584f04a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('category',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_by', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_category_created_by', 'category', ['created_by'], unique=False)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_table('tag',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('created_by', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'created_by', name='uq_tag_name_created_by')
    )
    op.create_index(op.f('ix_tag_created_by'), 'tag', ['created_by'], unique=False)
    op.create_table('task',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('owner_id', sa.BigInteger(), nullable=False),
    sa.Column('status', sa.Enum('todo', 'in_progress', 'done', 'cancelled', name='taskstatus'), server_default='todo', nullable=False),
    sa.Column('category_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_category_id'), 'task', ['category_id'], unique=False)
    op.create_index('ix_task_owner_id', 'task', ['owner_id'], unique=False)
    op.create_table('attachment',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.BigInteger(), nullable=False),
    sa.Column('owner_id', sa.BigInteger(), nullable=False),
    sa.Column('key', sa.String(length=1024), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('content_type', sa.String(length=127), nullable=False),
    sa.Column('size', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_index('ix_attachment_owner_id', 'attachment', ['owner_id'], unique=False)
    op.create_index('ix_attachment_task_id', 'attachment', ['task_id'], unique=False)
    op.create_table('comment',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('task_id', sa.BigInteger(), nullable=False),
    sa.Column('owner_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_comment_owner_id', 'comment', ['owner_id'], unique=False)
    op.create_index('ix_comment_task_id', 'comment', ['task_id'], unique=False)
    op.create_table('task_tag',
    sa.Column('task_id', sa.BigInteger(), nullable=False),
    sa.Column('tag_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('task_id', 'tag_id')
    )
    op.create_index('ix_task_tag_tag_id', 'task_tag', ['tag_id'], unique=False)
    op.create_index('ix_task_tag_task_id', 'task_tag', ['task_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_task_tag_task_id', table_name='task_tag')
    op.drop_index('ix_task_tag_tag_id', table_name='task_tag')
    op.drop_table('task_tag')
    op.drop_index('ix_comment_task_id', table_name='comment')
    op.drop_index('ix_comment_owner_id', table_name='comment')
    op.drop_table('comment')
    op.drop_index('ix_attachment_task_id', table_name='attachment')
    op.drop_index('ix_attachment_owner_id', table_name='attachment')
    op.drop_table('attachment')
    op.drop_index('ix_task_owner_id', table_name='task')
    op.drop_index(op.f('ix_task_category_id'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_tag_created_by'), table_name='tag')
    op.drop_table('tag')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index('ix_category_created_by', table_name='category')
    op.drop_table('category')