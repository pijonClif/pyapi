"""create users table

Revision ID: 64dadb8d484a
Revises: 1af87e38b6cd
Create Date: 2026-09-08 15:52:59.123806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = '64dadb8d484a'
down_revision: Union[str, Sequence[str], None] = '1af87e38b6cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
        )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass