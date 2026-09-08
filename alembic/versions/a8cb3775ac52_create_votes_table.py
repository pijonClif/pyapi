"""create votes table

Revision ID: a8cb3775ac52
Revises: 96c12f2091d3
Create Date: 2026-09-08 16:15:50.340557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8cb3775ac52'
down_revision: Union[str, Sequence[str], None] = '96c12f2091d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'votes',
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),

        sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    pass

def downgrade() -> None:
    op.drop_table('votes')
    pass