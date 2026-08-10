"""add tariff_reports table

Revision ID: 0139143e4725
Revises: 09e5a0ba9353
Create Date: 2026-08-10 13:51:37.949120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0139143e4725'
down_revision: Union[str, Sequence[str], None] = '09e5a0ba9353'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Hand-trimmed from autogenerate output — autogenerate also picked up
    # unrelated pre-existing drift (TEXT-vs-String column types on changelog/
    # regulated, missing indexes on message_reads/users.supplier_id) that has
    # nothing to do with this feature; left untouched here so this migration
    # only does one thing.
    op.create_table('tariff_reports',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('tariffId', sa.String(), nullable=False),
    sa.Column('tariffName', sa.String(), nullable=False),
    sa.Column('supplier', sa.String(), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('adminNote', sa.String(), nullable=True),
    sa.Column('createdAt', sa.String(), nullable=False),
    sa.Column('resolvedAt', sa.String(), nullable=True),
    sa.Column('resolvedBy', sa.String(), nullable=True),
    sa.Column('ipAddress', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tariff_reports')
