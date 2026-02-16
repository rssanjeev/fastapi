"""add phone_number column to users

Revision ID: 5696f8af3145
Revises: 6169ee5cca85
Create Date: 2026-01-17 11:49:51.725371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5696f8af3145'
down_revision: Union[str, Sequence[str], None] = '6169ee5cca85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add phone_number column if it doesn't exist
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True), if_not_exists=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop phone_number column if it exists
    op.drop_column('users', 'phone_number', if_exists=True)

