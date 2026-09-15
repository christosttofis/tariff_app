"""add tariff report category and reporter email

Revision ID: e8d3ce2bf35c
Revises: 7a2f9c1e4b8d
Create Date: 2026-09-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8d3ce2bf35c'
down_revision: Union[str, Sequence[str], None] = '7a2f9c1e4b8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('tariff_reports', sa.Column('category', sa.String(), nullable=True, server_default='other'))
    op.add_column('tariff_reports', sa.Column('reporterEmail', sa.String(), nullable=True))
    # Backfill pre-existing reports (submitted before this field existed) so
    # they don't show up as an empty/unknown category in the admin panel.
    op.execute("UPDATE tariff_reports SET category = 'other' WHERE category IS NULL")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('tariff_reports', 'reporterEmail')
    op.drop_column('tariff_reports', 'category')
