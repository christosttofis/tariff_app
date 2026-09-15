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
    op.alter_column('tariff_reports', 'tariffId', existing_type=sa.String(), nullable=True)
    op.alter_column('tariff_reports', 'tariffName', existing_type=sa.String(), nullable=True)
    op.alter_column('tariff_reports', 'supplier', existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('tariff_reports', 'supplier', existing_type=sa.String(), nullable=False)
    op.alter_column('tariff_reports', 'tariffName', existing_type=sa.String(), nullable=False)
    op.alter_column('tariff_reports', 'tariffId', existing_type=sa.String(), nullable=False)
