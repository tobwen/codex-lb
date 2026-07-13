"""make subagent prompt-cache TTL optional

Revision ID: 20260713_090000_make_subagent_prompt_cache_ttl_optional
Revises: 20260713_080000_add_subagent_prompt_cache_ttl
Create Date: 2026-07-13
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260713_090000_make_subagent_prompt_cache_ttl_optional"
down_revision = "20260713_080000_add_subagent_prompt_cache_ttl"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("dashboard_settings"):
        return
    columns = {column["name"] for column in inspector.get_columns("dashboard_settings")}
    column_name = "http_responses_session_bridge_fork_idle_ttl_seconds"
    if column_name not in columns:
        return
    with op.batch_alter_table("dashboard_settings") as batch_op:
        batch_op.alter_column(column_name, existing_type=sa.Integer(), nullable=True, server_default=None)
    op.execute(sa.text(f"UPDATE dashboard_settings SET {column_name} = NULL"))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("dashboard_settings"):
        return
    columns = {column["name"] for column in inspector.get_columns("dashboard_settings")}
    column_name = "http_responses_session_bridge_fork_idle_ttl_seconds"
    if column_name not in columns:
        return
    op.execute(sa.text(f"UPDATE dashboard_settings SET {column_name} = 120 WHERE {column_name} IS NULL"))
    with op.batch_alter_table("dashboard_settings") as batch_op:
        batch_op.alter_column(
            column_name,
            existing_type=sa.Integer(),
            nullable=False,
            server_default="120",
        )
