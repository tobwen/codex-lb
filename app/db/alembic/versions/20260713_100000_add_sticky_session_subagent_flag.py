"""mark prompt-cache mappings created by subagents

Revision ID: 20260713_100000_add_sticky_session_subagent_flag
Revises: 20260713_090000_make_subagent_prompt_cache_ttl_optional
Create Date: 2026-07-13
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260713_100000_add_sticky_session_subagent_flag"
down_revision = "20260713_090000_make_subagent_prompt_cache_ttl_optional"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("dashboard_settings"):
        settings_columns = {column["name"] for column in inspector.get_columns("dashboard_settings")}
        if (
            "http_responses_session_bridge_fork_idle_ttl_seconds" in settings_columns
            and "http_responses_session_bridge_subagent_prompt_cache_ttl_seconds" not in settings_columns
        ):
            with op.batch_alter_table("dashboard_settings") as batch_op:
                batch_op.alter_column(
                    "http_responses_session_bridge_fork_idle_ttl_seconds",
                    new_column_name="http_responses_session_bridge_subagent_prompt_cache_ttl_seconds",
                    existing_type=sa.Integer(),
                    nullable=True,
                )
    if not inspector.has_table("sticky_sessions"):
        return
    columns = {column["name"] for column in inspector.get_columns("sticky_sessions")}
    if "is_subagent" not in columns:
        with op.batch_alter_table("sticky_sessions") as batch_op:
            batch_op.add_column(
                sa.Column(
                    "is_subagent",
                    sa.Boolean(),
                    nullable=False,
                    server_default=sa.text("0"),
                )
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("dashboard_settings"):
        settings_columns = {column["name"] for column in inspector.get_columns("dashboard_settings")}
        if "http_responses_session_bridge_subagent_prompt_cache_ttl_seconds" in settings_columns:
            with op.batch_alter_table("dashboard_settings") as batch_op:
                batch_op.alter_column(
                    "http_responses_session_bridge_subagent_prompt_cache_ttl_seconds",
                    new_column_name="http_responses_session_bridge_fork_idle_ttl_seconds",
                    existing_type=sa.Integer(),
                    nullable=True,
                )
    if not inspector.has_table("sticky_sessions"):
        return
    columns = {column["name"] for column in inspector.get_columns("sticky_sessions")}
    if "is_subagent" in columns:
        with op.batch_alter_table("sticky_sessions") as batch_op:
            batch_op.drop_column("is_subagent")
