"""drop unique constraint on chat_request

Revision ID: drop_unique_001
Revises: c0cc0577493c
Create Date: 2026-06-26

"""

from collections.abc import Sequence

from alembic import op

revision: str = "drop_unique_001"
down_revision: str | None = "c0cc0577493c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("uq_chat_request_pair", "chat_request", schema="chats")


def downgrade() -> None:
    op.create_unique_constraint("uq_chat_request_pair", "chat_request", ["requester_id", "target_id"], schema="chats")
