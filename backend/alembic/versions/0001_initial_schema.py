"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("name", sa.String(100)),
        sa.Column("plan", sa.String(20), server_default="free"),
        sa.Column("stripe_customer_id", sa.String(100)),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "monitors",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("url", sa.String(2048), nullable=False),
        sa.Column("method", sa.String(10), server_default="GET"),
        sa.Column("interval", sa.Integer(), server_default="300"),
        sa.Column("timeout", sa.Integer(), server_default="30"),
        sa.Column("headers", sa.JSON()),
        sa.Column("body", sa.Text()),
        sa.Column("expected_status", sa.Integer(), server_default="200"),
        sa.Column("monitor_type", sa.String(20), server_default="http"),
        sa.Column("heartbeat_token", sa.String(64), unique=True, nullable=True),
        sa.Column("heartbeat_interval", sa.Integer(), nullable=True),
        sa.Column("heartbeat_grace", sa.Integer(), nullable=True, server_default="5"),
        sa.Column("last_ping_at", sa.DateTime(), nullable=True),
        sa.Column("keyword", sa.String(500)),
        sa.Column("keyword_present", sa.Boolean(), server_default=sa.true()),
        sa.Column("use_regex", sa.Boolean(), server_default=sa.false()),
        sa.Column("ssl_check", sa.Boolean(), server_default=sa.true()),
        sa.Column("ssl_expiry_days", sa.Integer(), server_default="14"),
        sa.Column("ssl_expires_at", sa.DateTime()),
        sa.Column("ssl_last_checked", sa.DateTime()),
        sa.Column("alert_threshold", sa.Integer(), server_default="1"),
        sa.Column("consecutive_failures", sa.Integer(), server_default="0"),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true()),
        sa.Column("last_status", sa.String(20)),
        sa.Column("last_checked_at", sa.DateTime()),
        sa.Column("next_check_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "checks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("monitor_id", sa.String(36), sa.ForeignKey("monitors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("status_code", sa.Integer()),
        sa.Column("response_time", sa.Integer()),
        sa.Column("error_message", sa.Text()),
        sa.Column("checked_at", sa.DateTime(), server_default=sa.func.now(), index=True),
    )

    op.create_table(
        "alert_channels",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "monitor_alert_channels",
        sa.Column("monitor_id", sa.String(36), sa.ForeignKey("monitors.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("alert_channel_id", sa.String(36), sa.ForeignKey("alert_channels.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "team_members",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("member_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True),
        sa.Column("invited_email", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), server_default="member"),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("invite_token", sa.String(100), unique=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("accepted_at", sa.DateTime()),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("lemonsqueezy_subscription_id", sa.String(100), unique=True),
        sa.Column("plan", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("current_period_end", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "api_keys",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("key_hash", sa.String(255), nullable=False, unique=True),
        sa.Column("key_prefix", sa.String(10), nullable=False),
        sa.Column("last_used_at", sa.DateTime()),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "maintenance_windows",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("repeat_type", sa.String(20), server_default="once"),
        sa.Column("weekday", sa.Integer()),
        sa.Column("day_of_month", sa.Integer()),
        sa.Column("start_time", sa.String(5), nullable=False),
        sa.Column("end_time", sa.String(5), nullable=False),
        sa.Column("start_date", sa.DateTime()),
        sa.Column("end_date", sa.DateTime()),
        sa.Column("timezone", sa.String(50), server_default="UTC"),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "maintenance_window_monitors",
        sa.Column("maintenance_window_id", sa.String(36), sa.ForeignKey("maintenance_windows.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("monitor_id", sa.String(36), sa.ForeignKey("monitors.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "monitor_assertions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("monitor_id", sa.String(36), sa.ForeignKey("monitors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("assertion_type", sa.String(20), nullable=False, server_default="jsonpath"),
        sa.Column("path", sa.Text(), nullable=True),
        sa.Column("operator", sa.String(20), nullable=False),
        sa.Column("value", sa.JSON(), nullable=True),
        sa.Column("logic", sa.String(3), server_default="AND"),
        sa.Column("order", sa.Integer(), server_default="0"),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("monitor_assertions")
    op.drop_table("maintenance_window_monitors")
    op.drop_table("maintenance_windows")
    op.drop_table("api_keys")
    op.drop_table("subscriptions")
    op.drop_table("team_members")
    op.drop_table("monitor_alert_channels")
    op.drop_table("alert_channels")
    op.drop_table("checks")
    op.drop_table("monitors")
    op.drop_table("users")
