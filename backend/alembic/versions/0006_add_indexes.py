"""add indexes for monitors.user_id, monitors.is_active, checks.monitor_id

Revision ID: 0006
Revises: 0005
Create Date: 2026-05-03 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("ix_monitors_user_id", "monitors", ["user_id"])
    op.create_index("ix_monitors_is_active", "monitors", ["is_active"])
    op.create_index("ix_checks_monitor_id", "checks", ["monitor_id"])


def downgrade() -> None:
    op.drop_index("ix_monitors_user_id", table_name="monitors")
    op.drop_index("ix_monitors_is_active", table_name="monitors")
    op.drop_index("ix_checks_monitor_id", table_name="checks")
