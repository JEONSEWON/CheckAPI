"""add webhook_logs table

Revision ID: 0007
Revises: 0006
Create Date: 2026-05-03 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "webhook_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("event_name", sa.String(100), nullable=False),
        sa.Column("lemonsqueezy_subscription_id", sa.String(100)),
        sa.Column("user_id", sa.String(36)),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("processed_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("success", sa.Boolean(), server_default="true"),
        sa.Column("error_message", sa.Text()),
    )
    op.create_index("ix_webhook_logs_event_name", "webhook_logs", ["event_name"])
    op.create_index("ix_webhook_logs_processed_at", "webhook_logs", ["processed_at"])


def downgrade() -> None:
    op.drop_index("ix_webhook_logs_processed_at", table_name="webhook_logs")
    op.drop_index("ix_webhook_logs_event_name", table_name="webhook_logs")
    op.drop_table("webhook_logs")
