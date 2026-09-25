"""allow general (non-tariff-specific) tariff reports

Revision ID: 83ce50ff9ed3
Revises: e8d3ce2bf35c
Create Date: 2026-09-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83ce50ff9ed3'
down_revision: Union[str, Sequence[str], None] = 'e8d3ce2bf35c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # A general site issue (customer.html footer "Report a general issue"
    # link) has no associated tariff, so these three can no longer be
    # required.
    # batch_alter_table so this also works on SQLite (used by
    # seed_demo_data.py for the reviewer/demo path); SQLite has no
    # ALTER COLUMN ... DROP NOT NULL, so Alembic emits a table copy instead.
    with op.batch_alter_table('tariff_reports') as batch_op:
        batch_op.alter_column('tariffId', existing_type=sa.String(), nullable=True)
        batch_op.alter_column('tariffName', existing_type=sa.String(), nullable=True)
        batch_op.alter_column('supplier', existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('tariff_reports') as batch_op:
        batch_op.alter_column('supplier', existing_type=sa.String(), nullable=False)
        batch_op.alter_column('tariffName', existing_type=sa.String(), nullable=False)
        batch_op.alter_column('tariffId', existing_type=sa.String(), nullable=False)
