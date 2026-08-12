"""add sample invoice config

Revision ID: 7a2f9c1e4b8d
Revises: 011d08ad608f
Create Date: 2026-08-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a2f9c1e4b8d'
down_revision: Union[str, Sequence[str], None] = '011d08ad608f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'sample_invoice_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.execute("INSERT INTO sample_invoice_config (id, enabled) VALUES (1, FALSE)")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sample_invoice_config')
