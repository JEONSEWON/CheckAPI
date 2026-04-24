"""add custom_domain to monitors

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-24 00:01:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("monitors", sa.Column("custom_domain", sa.String(255), nullable=True, unique=True))


def downgrade() -> None:
    op.drop_column("monitors", "custom_domain")
