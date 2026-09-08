"""add foreign key to post table

Revision ID: 96c12f2091d3
Revises: 64dadb8d484a
Create Date: 2026-09-08 16:08:22.668571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96c12f2091d3'
down_revision: Union[str, Sequence[str], None] = '64dadb8d484a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_users_fk', 
        source_table="posts", referent_table="users",
        local_cols=['owner_id'], remote_cols=['id'],
        ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass