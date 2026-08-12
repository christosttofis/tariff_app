"""add supplier regulated flag

Revision ID: cda0b00350b7
Revises: 0139143e4725
Create Date: 2026-08-12 09:51:54.348412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cda0b00350b7'
down_revision: Union[str, Sequence[str], None] = '0139143e4725'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# NOTE: autogenerate also picked up pre-existing unrelated schema drift
# (changelog/regulated TEXT->String column types, missing message_reads/
# users indexes on supplier_id) — trimmed out here, same as prior migrations
# in this project. Only the intended column is included.


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('suppliers', sa.Column('regulated', sa.Boolean(), nullable=True, server_default=sa.false()))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('suppliers', 'regulated')
