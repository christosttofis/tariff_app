"""add tariff mdm invoice frequency

Revision ID: 011d08ad608f
Revises: b4b467493b08
Create Date: 2026-08-12 10:19:10.974574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '011d08ad608f'
down_revision: Union[str, Sequence[str], None] = 'b4b467493b08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# NOTE: autogenerate also picked up pre-existing unrelated schema drift
# (changelog/regulated TEXT->String column types, missing message_reads/
# users indexes on supplier_id) — trimmed out here, same as prior migrations
# in this project. Only the intended column is included.
#
# Default is 2 (bimonthly) — the common case for existing tariffs, all of
# which were previously calculated as if billed every month (mdm * 12).
# Admins/suppliers should review and set 1 (monthly) for tariffs that are
# actually invoiced monthly (typically industrial).


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('tariffs', sa.Column('mdmInvoiceMonths', sa.Integer(), nullable=True, server_default='2'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('tariffs', 'mdmInvoiceMonths')
