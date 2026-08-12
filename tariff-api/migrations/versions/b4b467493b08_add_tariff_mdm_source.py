"""add tariff mdm source

Revision ID: b4b467493b08
Revises: cda0b00350b7
Create Date: 2026-08-12 10:09:26.249394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4b467493b08'
down_revision: Union[str, Sequence[str], None] = 'cda0b00350b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# NOTE: autogenerate also picked up pre-existing unrelated schema drift
# (changelog/regulated TEXT->String column types, missing message_reads/
# users indexes on supplier_id) — trimmed out here, same as prior migrations
# in this project. Only the intended column (+ its one-time backfill) is
# included.


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('tariffs', sa.Column('mdmSource', sa.String(), nullable=True, server_default='custom'))
    # Existing tariffs under an already-regulated supplier (e.g. EAC) default
    # to following the CERA-set regulated MDM rate, matching the new backend
    # enforcement — everyone else keeps their own per-tariff mdm value as-is.
    op.execute(
        "UPDATE tariffs SET \"mdmSource\" = 'global' "
        "WHERE supplier IN (SELECT name FROM suppliers WHERE regulated = true)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('tariffs', 'mdmSource')
