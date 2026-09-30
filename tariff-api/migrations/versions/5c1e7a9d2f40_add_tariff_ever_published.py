"""add tariff everPublished flag

Revision ID: 5c1e7a9d2f40
Revises: 83ce50ff9ed3
Create Date: 2026-09-30 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c1e7a9d2f40'
down_revision: Union[str, Sequence[str], None] = '83ce50ff9ed3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Records whether a tariff has ever been approved (public), so a supplier
# deleting one that was since edited back to pending archives it instead of
# erasing it. Backfilled from current status plus the changelog: any recorded
# change of status to "approved", or creation by an admin (admin-created
# tariffs start approved).


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('tariffs', sa.Column('everPublished', sa.Boolean(), nullable=False, server_default=sa.false()))

    tariffs = sa.table('tariffs', sa.column('id', sa.String), sa.column('status', sa.String),
                       sa.column('everPublished', sa.Boolean))
    changelog = sa.table('changelog', sa.column('tariffId', sa.String), sa.column('action', sa.String),
                         sa.column('actorRole', sa.String), sa.column('changes', sa.Text))
    approved_in_history = sa.select(changelog.c.tariffId).where(
        sa.or_(
            changelog.c.changes.like('%"to": "approved"%'),
            sa.and_(changelog.c.action == 'created', changelog.c.actorRole == 'admin'),
        )
    )
    op.execute(
        tariffs.update()
        .where(sa.or_(tariffs.c.status.in_(['approved', 'suspended', 'archived']),
                      tariffs.c.id.in_(approved_in_history)))
        .values(everPublished=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('tariffs') as batch_op:
        batch_op.drop_column('everPublished')
