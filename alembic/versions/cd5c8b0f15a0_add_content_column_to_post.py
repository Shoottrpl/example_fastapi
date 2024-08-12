"""add content column to post

Revision ID: cd5c8b0f15a0
Revises: a783f59cd4e7
Create Date: 2024-08-12 22:39:02.743415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd5c8b0f15a0'
down_revision: Union[str, None] = 'a783f59cd4e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
