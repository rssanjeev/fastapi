"""Initial Setup

Revision ID: 6169ee5cca85
Revises: 
Create Date: 2026-01-17 11:44:23.273580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6169ee5cca85'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, nullable=False, unique=True, index=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, nullable=False, server_default='True'),
        sa.Column('rating', sa.Integer, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    )
    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column('post_id', sa.Integer, sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
