"""add DAM versions (backup/rollback), DAM change log and stale-alert marker

Revision ID: d4a7b2e9c135
Revises: 5c1e7a9d2f40
Create Date: 2026-10-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4a7b2e9c135'
down_revision: Union[str, Sequence[str], None] = '5c1e7a9d2f40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# The DAM data already stored is copied into dam_versions by the app itself
# (routers/admin.py _ensure_initial_version) the first time anything replaces
# it, so it is backed up before the first change whatever created the row.


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'dam_versions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.String(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('restored_from', sa.Integer(), nullable=True),
        sa.Column('first_date', sa.String(), nullable=True),
        sa.Column('last_date', sa.String(), nullable=True),
        sa.Column('day_count', sa.Integer(), nullable=True),
        sa.Column('row_count', sa.Integer(), nullable=True),
        sa.Column('payload', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'dam_change_log',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ts', sa.String(), nullable=False),
        sa.Column('actor', sa.String(), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('version_id', sa.Integer(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.add_column('dam_data', sa.Column('stale_notified_at', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('dam_data') as batch_op:
        batch_op.drop_column('stale_notified_at')
    op.drop_table('dam_change_log')
    op.drop_table('dam_versions')
