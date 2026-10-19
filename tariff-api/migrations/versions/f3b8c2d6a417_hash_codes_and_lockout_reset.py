"""store reset tokens and sign-in codes hashed; add users.lockout_reset_at

Revision ID: f3b8c2d6a417
Revises: d4a7b2e9c135
Create Date: 2026-10-19 12:00:00.000000

"""
import hashlib
import re
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3b8c2d6a417'
down_revision: Union[str, Sequence[str], None] = 'd4a7b2e9c135'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_DIGEST = re.compile(r"^[0-9a-f]{64}$")


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('users') as batch:
        batch.add_column(sa.Column('lockout_reset_at', sa.String(), nullable=True))

    # Reset and invite links already emailed keep working: their tokens are
    # replaced by the same SHA-256 the app now looks them up by
    # (auth.reset_token_digest). Already-hashed rows are left alone.
    conn = op.get_bind()
    for (token,) in conn.execute(sa.text("SELECT token FROM password_resets")).fetchall():
        if not _DIGEST.match(token):
            conn.execute(sa.text("UPDATE password_resets SET token = :new WHERE token = :old"),
                         {"new": hashlib.sha256(token.encode()).hexdigest(), "old": token})

    # Sign-in codes last 10 minutes; anyone mid-sign-in just requests a new one.
    conn.execute(sa.text("DELETE FROM otp_codes"))


def downgrade() -> None:
    """Downgrade schema."""
    # Hashed tokens and codes can't be turned back into the emailed values.
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM password_resets"))
    conn.execute(sa.text("DELETE FROM otp_codes"))
    with op.batch_alter_table('users') as batch:
        batch.drop_column('lockout_reset_at')
